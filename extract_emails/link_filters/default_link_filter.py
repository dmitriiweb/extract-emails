from typing import List, Set
from urllib.parse import urljoin, urlparse

from extract_emails.link_filters import LinkFilterInterface


class DefaultLinkFilter(LinkFilterInterface):
    """
    Default filter for links

    :param list(str) links: List of URLs
    """

    checked_links: Set[str] = set()

    def filter(self, links: List[str]) -> List[str]:
        filtered_urls = []
        for url in links:
            url = urljoin(self.website, url)
            if url.startswith(self.website) and url not in self.checked_links:
                self.checked_links.add(url)
                filtered_urls.append(url)
        return filtered_urls

    @staticmethod
    def get_website_address(url: str) -> str:
        """
        Get website address from an URL

        Example:
            >>> DefaultLinkFilter.get_website_address('https://example.com/page.html?param=123')
            ... 'https://example.com/'

        :param str url: some URL
        :return: website address
        """
        parsed_url = urlparse(url)
        return f"{parsed_url.scheme}://{parsed_url.netloc}/"
