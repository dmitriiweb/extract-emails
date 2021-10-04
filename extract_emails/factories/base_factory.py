from abc import ABC
from abc import abstractmethod
from typing import TYPE_CHECKING
from typing import List
from typing import Optional
from typing import Type

from extract_emails.browsers import PageSourceGetter
from extract_emails.data_extractors import DataExtractor
from extract_emails.link_filters import LinkFilterBase


class BaseFactory(ABC):
    """Base class for all factories"""

    def __init__(
        self,
        *,
        website_url: str,
        browser: PageSourceGetter,
        depth: Optional[int] = None,
        max_links_from_page: Optional[int] = None,
    ):
        """
        Args:
            website_url: website for scan, e.g. https://example.com
            browser: browser to get page source by URL
            depth: scan's depth, default 10
            max_links_from_page: how many links a script shall get from each page, default None (all)
        """
        self._website_url = website_url
        self._browser = browser
        self._depth = depth
        self._max_links_from_page = max_links_from_page

    @property
    @abstractmethod
    def link_filter(self) -> Type[LinkFilterBase]:
        """Initialize link filter"""

    @property
    @abstractmethod
    def data_extractors(self) -> List[Type[DataExtractor]]:
        """Initialize data extractors"""

    @property
    def website_url(self) -> str:
        return self._website_url

    @property
    def browser(self) -> PageSourceGetter:
        return self._browser

    @property
    def depth(self) -> Optional[int]:
        return self._depth

    @property
    def max_links_from_page(self) -> Optional[int]:
        return self._max_links_from_page
