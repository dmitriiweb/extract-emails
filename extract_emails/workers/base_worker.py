from abc import ABC
from abc import abstractmethod
from typing import List
from typing import Type

from loguru import logger

from extract_emails.browsers import PageSourceGetter
from extract_emails.data_extractors import DataExtractor
from extract_emails.link_filters import LinkFilterBase
from extract_emails.models import PageData


class BaseExtractor(ABC):
    """Base class for all workers"""

    def __init__(
        self,
        website_url: str,
        browser: PageSourceGetter,
        depth: int = 10,
        max_links_from_page: int = -1,
    ):
        """
        Args:
            website_url: website for scan, e.g. https://example.com
            browser: browser to get page source by URL
            depth: scan's depth, default 10
            max_links_from_page: how many links a script shall get from each page, default -1 (all)
        """
        self.website_url = website_url
        self.browser = browser
        self.depth = depth
        self.max_links_from_page = max_links_from_page

        self.link_filter = self.get_link_filter()
        self.data_extractors = self.get_data_extractors()

        self.links = [[self.website_url]]
        self.current_depth = 0

    @abstractmethod
    def get_link_filter(self) -> Type[LinkFilterBase]:
        pass

    @abstractmethod
    def get_data_extractors(self) -> List[Type[DataExtractor]]:
        pass

    def get_data(self) -> List[PageData]:
        """Extract data from a given website"""
        data: List[PageData] = []

        while len(self.links):
            if self.current_depth > self.depth:
                break

            self.current_depth += 1
            urls = self.links.pop(0)
            new_urls: List[str] = []

            for url in urls:
                try:
                    page_source = self.browser.get_page_source(url)
                except Exception as e:
                    logger.error("Cannot get data from {}: {}".format(url, e))
                    continue

                new_links = self.link_filter.get_links(page_source)
                filtered_links = self.link_filter.filter(new_links)
                new_urls.extend(filtered_links)

                page_data = PageData(website=self.website_url, page_url=url)

                for data_extractor in self.data_extractors:
                    new_data = data_extractor.get_data(page_source)
                    page_data.append(data_extractor.name, list(new_data))

                data.append(page_data)

            self.links.append(new_urls)

        return data
