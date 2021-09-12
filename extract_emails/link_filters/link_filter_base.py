from abc import ABC
from abc import abstractmethod
from typing import Iterable
from typing import Set
from urllib.parse import urlparse


class LinkFilterBase(ABC):
    """Base class for link filters"""

    def __init__(self, website: str, *args, **kwargs):
        """

        Args:
            website: website address (scheme and domain), e.g. https://example.com
            *args: additional non-keywords arguments
            **kwargs: additional keywords arguments
        """
        self.website = website

    @staticmethod
    def get_website_address(url: str) -> str:
        """Extract scheme and domain name from an URL

        Examples:
            >>> from extract_emails.link_filters import LinkFilterBase
            >>> website = LinkFilterBase.get_website_address('https://example.com/list?page=134')
            >>> website
            'https://example.com/'

        Args:
            url: URL for parsing

        Returns:
            scheme and domain name from URL, e.g. https://example.com

        """
        parsed_url = urlparse(url)
        return f"{parsed_url.scheme}://{parsed_url.netloc}/"

    @abstractmethod
    def filter(self, urls: Iterable[str]) -> Set[str]:
        """Filter links by some parameters

        Args:
            urls: List of URLs for filtering

        Returns:
            List of filtered URLs
        """
