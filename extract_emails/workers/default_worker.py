from __future__ import annotations

from collections import deque
from urllib.parse import urldefrag, urljoin, urlsplit

from loguru import logger

from extract_emails.browsers.page_source_getter import PageSourceGetter
from extract_emails.data_extractors import (
    DataExtractor,
    EmailExtractor,
    LinkedinExtractor,
)
from extract_emails.link_filters import ContactInfoLinkFilter, LinkFilterBase
from extract_emails.models import PageData


class DefaultWorker:
    """DefaultWorker is responsible for orchestrating the extraction of emails and LinkedIn URLs from a given website.

    This class utilizes both synchronous and asynchronous workers to perform the extraction process. It manages the
    configuration of the extraction process, including the website URL, browser, link filter, data extractors, depth,
    and maximum links to extract from a page.

    Attributes:
        website_url (str): The URL of the website to extract data from.
        browser (PageSourceGetter): The browser instance used to fetch page sources.
        link_filter (LinkFilterBase): The filter used to determine which links to follow.
        data_extractors (list[DataExtractor]): The list of data extractors to use for extracting information.
        depth (int): The maximum depth to traverse the website.
        max_links_from_page (int): The maximum number of links to extract from a single page.
        links (list[list[str]]): The initial URL batch retained for compatibility.
        current_depth (int): The current traversal depth.
    """

    def __init__(
        self,
        website_url: str,
        browser: PageSourceGetter,
        *,
        link_filter: LinkFilterBase | None = None,
        data_extractors: list[DataExtractor] | None = None,
        depth: int = 20,
        max_links_from_page: int = 20,
    ):
        self.website_url = website_url
        self.browser = browser
        self.link_filter = link_filter or ContactInfoLinkFilter(self.website_url)
        self.data_extractors = data_extractors or [
            EmailExtractor(),
            LinkedinExtractor(),
        ]
        if depth is not None and depth < 0:
            raise ValueError("depth must be non-negative")
        if max_links_from_page < 0:
            raise ValueError("max_links_from_page must be non-negative")
        self.depth = depth
        self.max_links_from_page = max_links_from_page

        self.links = [[self.website_url]]
        self.current_depth = 0

        self._sync_worker = _SyncDefaultWorker(
            self.website_url,
            self.browser,
            link_filter=self.link_filter,
            data_extractors=self.data_extractors,
            depth=self.depth,
            max_links_from_page=self.max_links_from_page,
        )
        self._async_worker = _AsyncDefaultWorker(
            self.website_url,
            self.browser,
            link_filter=self.link_filter,
            data_extractors=self.data_extractors,
            depth=self.depth,
            max_links_from_page=self.max_links_from_page,
        )

    def get_data(self) -> list[PageData]:
        """Retrieve extracted data synchronously.

        Returns:
            list[PageData]: A list of PageData objects containing the extracted information.
        """
        return self._sync_worker.get_data()

    async def aget_data(self) -> list[PageData]:
        """Retrieve extracted data asynchronously.

        Returns:
            list[PageData]: A list of PageData objects containing the extracted information.
        """
        return await self._async_worker.get_data()


class _DefaultWorker:
    def __init__(
        self,
        website_url: str,
        browser: PageSourceGetter,
        *,
        link_filter: LinkFilterBase,
        data_extractors: list[DataExtractor],
        depth: int,
        max_links_from_page: int,
    ):
        self.website_url = website_url
        self.browser = browser
        self.link_filter = link_filter
        self.data_extractors = data_extractors
        self.depth = depth
        self.max_links_from_page = max_links_from_page

        self.links: deque[tuple[str, int]] = deque([(self.website_url, 0)])
        self._scheduled = {self._scheduled_key(self.website_url)}
        self.current_depth = 0

    @staticmethod
    def _scheduled_key(url: str) -> str:
        """Treat an origin's empty path and slash path as the same page."""
        parts = urlsplit(url)
        if not parts.path:
            return parts._replace(path="/").geturl()
        return url

    def _get_page_links(self, page_source: str, requested_url: str) -> list[str]:
        """Resolve and filter references from one fetched page.

        Args:
            page_source: HTML or other page content returned by the browser.
            requested_url: URL requested from the browser for this page.

        Returns:
            Absolute, same-site URLs accepted by the configured link filter.
        """
        absolute_links = []
        for href in self.link_filter.get_links(page_source):
            resolved, _fragment = urldefrag(urljoin(requested_url, href))
            if urlsplit(resolved).scheme.lower() in {"http", "https"}:
                absolute_links.append(resolved)
        return self.link_filter.filter(absolute_links)

    def _make_page_data(self, url: str, page_source: str) -> PageData:
        """Build a page result using the shared extractor set.

        Args:
            url: Requested URL represented by the result.
            page_source: Content returned for the requested page.

        Returns:
            Extracted data associated with the requested page.
        """
        page_data = PageData(website=self.website_url, page_url=url)
        for data_extractor in self.data_extractors:
            new_data = data_extractor.get_data(page_source)  # type: ignore
            page_data.append(data_extractor.name, list(new_data))  # type: ignore
        return page_data

    def _schedule_links(self, urls: list[str], distance: int) -> None:
        """Schedule unseen URLs at the next crawl distance.

        Args:
            urls: Filter-approved absolute URLs discovered on the current page.
            distance: Link distance of the current page.
        """
        if self.max_links_from_page:
            urls = urls[: self.max_links_from_page]
        for url in urls:
            key = self._scheduled_key(url)
            if key not in self._scheduled:
                self._scheduled.add(key)
                self.links.append((url, distance + 1))


class _SyncDefaultWorker(_DefaultWorker):
    def get_data(self) -> list[PageData]:
        """Extract data from a given website."""
        data: list[PageData] = []
        while self.links:
            url, distance = self.links.popleft()
            if self.depth is not None and distance > self.depth:
                continue
            self.current_depth = distance
            logger.info(f"getting data from {url}")
            try:
                page_source = self.browser.get_page_source(url)
                new_urls = self._get_page_links(page_source, url)
                page_data = self._make_page_data(url, page_source)
            except Exception as e:
                logger.error("Cannot get data from {}: {}".format(url, e))
                continue
            logger.info("URL: {} | found {} items", url, len(page_data))
            data.append(page_data)
            self._schedule_links(new_urls, distance)
        return data

    def _get_page_data(self, url: str) -> tuple[list[str], PageData]:
        page_source = self.browser.get_page_source(url)
        filtered_links = self._get_page_links(page_source, url)
        page_data = self._make_page_data(url, page_source)
        return filtered_links, page_data


class _AsyncDefaultWorker(_DefaultWorker):
    async def get_data(self) -> list[PageData]:
        """Extract data from a given website."""
        data: list[PageData] = []
        while self.links:
            url, distance = self.links.popleft()
            if self.depth is not None and distance > self.depth:
                continue
            self.current_depth = distance
            logger.info(f"getting data from {url}")
            try:
                page_source = await self.browser.aget_page_source(url)
                new_urls = self._get_page_links(page_source, url)
                page_data = self._make_page_data(url, page_source)
            except Exception as e:
                logger.error("Cannot get data from {}: {}".format(url, e))
                continue
            logger.info("URL: {} | found {} items", url, len(page_data))
            data.append(page_data)
            self._schedule_links(new_urls, distance)
        return data

    async def _get_page_data(self, url: str) -> tuple[list[str], PageData]:
        page_source = await self.browser.aget_page_source(url)
        filtered_links = self._get_page_links(page_source, url)
        page_data = self._make_page_data(url, page_source)
        return filtered_links, page_data
