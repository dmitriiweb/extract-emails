from typing import List
from typing import Tuple

from loguru import logger

from extract_emails.factories import BaseFactory
from extract_emails.models import PageData


class DefaultWorker:
    """All data extractions goes here."""

    def __init__(self, factory: BaseFactory):
        """
        Args:
            factory: see `BaseFactory`
        """
        self.website_url = factory.website_url
        self.browser = factory.browser
        self.depth = factory.depth
        self.max_links_from_page = factory.max_links_from_page
        self.link_filter = factory.link_filter
        self.data_extractors = factory.data_extractors

        self.links = [[self.website_url]]
        self.current_depth = 0

    def get_data(self) -> List[PageData]:
        """Extract data from a given website"""
        data: List[PageData] = []

        while len(self.links):
            logger.debug(f"current_depth={self.current_depth}")
            if self.depth is not None and self.current_depth > self.depth:
                break
            self.current_depth += 1

            new_data = self._get_new_data()
            data.extend(new_data)

        return data

    def _get_new_data(self) -> List[PageData]:

        data: List[PageData] = []
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

    def _get_page_data(self, url: str) -> Tuple[List[str], PageData]:
        page_source = self.browser.get_page_source(url)

        new_links = self.link_filter.get_links(page_source)
        filtered_links = self.link_filter.filter(new_links)

        page_data = PageData(website=self.website_url, page_url=url)

        for data_extractor in self.data_extractors:
            new_data = data_extractor.get_data(page_source)
            page_data.append(data_extractor.name, list(new_data))

        return filtered_links, page_data
