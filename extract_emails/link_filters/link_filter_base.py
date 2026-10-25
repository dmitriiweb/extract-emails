import re
from abc import ABC, abstractmethod
from typing import Iterable, cast
from urllib.parse import urlparse

from lxml import html
from lxml.etree import ParserError

_XML_DECLARATION = re.compile(r"\A(\ufeff?[ \t\r\n]*)<\?xml[ \t\r\n]+.*?\?>", re.DOTALL)


class LinkFilterBase(ABC):
    """Base class for link filters"""

    def __init__(self, website: str):
        """

        Args:
            website: website address (scheme and domain), e.g. https://example.com
        """
        self.website = self._normalize_website(website)
        self.allowed_netlocs = self._build_allowed_netlocs(self.website)

    @staticmethod
    def _normalize_website(website: str) -> str:
        if "://" not in website:
            website = f"https://{website}"
        return LinkFilterBase.get_website_address(website)

    @staticmethod
    def _build_allowed_netlocs(website: str) -> set[str]:
        netloc = urlparse(website).netloc
        if not netloc:
            return set()
        allowed = {netloc}
        if netloc.startswith("www."):
            allowed.add(netloc.removeprefix("www."))
        else:
            allowed.add(f"www.{netloc}")
        return allowed

    def _is_allowed(self, url: str) -> bool:
        netloc = urlparse(url).netloc
        if not netloc:
            return False
        return netloc in self.allowed_netlocs

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
    def get_links(page_source: str) -> list[str]:
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
        if not page_source:
            return []

        try:
            normalized_source = _XML_DECLARATION.sub(r"\1", page_source, count=1)
            document = html.fromstring(normalized_source)
        except (ParserError, ValueError):
            return []
        return cast(list[str], document.xpath("//a[@href]/@href"))

    @abstractmethod
    def filter(self, urls: Iterable[str]) -> list[str]:
        """Filter links by some parameters

        Args:
            urls: List of URLs for filtering

        Returns:
            List of filtered URLs
        """
