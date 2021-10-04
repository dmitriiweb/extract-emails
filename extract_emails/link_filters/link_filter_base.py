import re

from abc import ABC
from abc import abstractmethod
from typing import Iterable
from typing import List
from urllib.parse import urlparse


RE_LINKS = re.compile(r'<a\s+(?:[^>]*?\s+)?href=(["\'])(.*?)\1')


class LinkFilterBase(ABC):
    """Base class for link filters"""

    def __init__(self, website: str):
        """

        Args:
            website: website address (scheme and domain), e.g. https://example.com
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

    @staticmethod
    def get_links(page_source: str) -> List[str]:
        """Extract all URLs corresponding to current website

        Examples:
            >>> from extract_emails.link_filters import LinkFilterBase
            >>> links = LinkFilterBase.get_links(page_source)
            >>> links
            ["example.com", "/example.com", "https://example2.com"]

        Args:
            page_source: HTML page source

        Returns:
            List of URLs

        :param str page_source: HTML page source
        :return: List of URLs
        """
        links = RE_LINKS.findall(page_source)
        links = [x[1] for x in links]
        return links

    @abstractmethod
    def filter(self, urls: Iterable[str]) -> List[str]:
        """Filter links by some parameters

        Args:
            urls: List of URLs for filtering

        Returns:
            List of filtered URLs
        """
