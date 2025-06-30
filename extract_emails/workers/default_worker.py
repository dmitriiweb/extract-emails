from __future__ import annotations

from abc import ABC

from loguru import logger

from extract_emails.browsers import PageSourceGetter
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
        links (list[list[str]]): A list of lists containing URLs to be processed at each depth level.
        current_depth (int): The current depth level of the extraction process.
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
        self.website_url = website_url.rstrip("/")
        self.browser = browser
        self.link_filter = link_filter or ContactInfoLinkFilter(self.website_url)
        self.data_extractors = data_extractors or [
            EmailExtractor(),
            LinkedinExtractor(),
        ]
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
        return self._sync_worker.get_data()

    async def aget_data(self) -> list[PageData]:
        return await self._async_worker.get_data()


class _DefaultWorker(ABC):
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
        self.website_url = website_url.rstrip("/")
        self.browser = browser
        self.link_filter = link_filter
        self.data_extractors = data_extractors
        self.depth = depth
        self.max_links_from_page = max_links_from_page

        self.links = [[self.website_url]]
        self.current_depth = 0


class _SyncDefaultWorker(_DefaultWorker):
    def get_data(self) -> list[PageData]:
        """Extract data from a given website"""
        data: list[PageData] = []

        while len(self.links):
            logger.debug(f"current_depth={self.current_depth}")
            if self.depth is not None and self.current_depth > self.depth:
                break
            self.current_depth += 1

            new_data = self._get_new_data()
            data.extend(new_data)

        return data

    def _get_new_data(self) -> list[PageData]:
        data: list[PageData] = []
        urls = self.links.pop(0)

        for url in urls:
            logger.info(f"getting data from {url}")
            try:
                new_urls, page_data = self._get_page_data(url)
            except Exception as e:
                logger.error("Cannot get data from {}: {}".format(url, e))
                continue

            logger.info(f"URL: {url} | found {len(page_data)} items")
            data.append(page_data)

            if self.max_links_from_page:
                new_urls = new_urls[: self.max_links_from_page]

            logger.debug(f"Add {len(new_urls)} new URLs to the queue")
            self.links.append(new_urls)

        return data

    def _get_page_data(self, url: str) -> tuple[list[str], PageData]:
        page_source = self.browser.get_page_source(url)

        new_links = self.link_filter.get_links(page_source)
        filtered_links = self.link_filter.filter(new_links)  # type: ignore

        page_data = PageData(website=self.website_url, page_url=url)

        for data_extractor in self.data_extractors:
            new_data = data_extractor.get_data(page_source)  # type: ignore
            page_data.append(data_extractor.name, list(new_data))  # type: ignore

        return filtered_links, page_data


class _AsyncDefaultWorker(_DefaultWorker):
    async def get_data(self) -> list[PageData]:
        """Extract data from a given website"""
        data: list[PageData] = []

        while len(self.links):
            logger.debug(f"current_depth={self.current_depth}")
            if self.depth is not None and self.current_depth > self.depth:
                break
            self.current_depth += 1

            new_data = await self._get_new_data()
            data.extend(new_data)

        return data

    async def _get_new_data(self) -> list[PageData]:
        data: list[PageData] = []
        urls = self.links.pop(0)

        for url in urls:
            logger.info(f"getting data from {url}")
            try:
                new_urls, page_data = await self._get_page_data(url)
            except Exception as e:
                logger.error("Cannot get data from {}: {}".format(url, e))
                continue

            logger.info(f"URL: {url} | found {len(page_data)} items")
            data.append(page_data)

            if self.max_links_from_page:
                new_urls = new_urls[: self.max_links_from_page]

            logger.debug(f"Add {len(new_urls)} new URLs to the queue")
            self.links.append(new_urls)

        return data

    async def _get_page_data(self, url: str) -> tuple[list[str], PageData]:
        page_source = await self.browser.aget_page_source(url)

        new_links = self.link_filter.get_links(page_source)
        filtered_links = self.link_filter.filter(new_links)  # type: ignore

        page_data = PageData(website=self.website_url, page_url=url)

        for data_extractor in self.data_extractors:
            new_data = await data_extractor.aget_data(page_source)  # type: ignore
            page_data.append(data_extractor.name, list(new_data))  # type: ignore

        return filtered_links, page_data
