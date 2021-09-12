from typing import Iterable
from typing import List
from typing import Set
from urllib.parse import urljoin
from urllib.parse import urlparse

from extract_emails.link_filters.link_filter_base import LinkFilterBase


class DefaultLinkFilter(LinkFilterBase):
    """Default filter for links"""

    def filter(self, links: Iterable[str]) -> Set[str]:
        """Will exclude from a list URLs, which not starts with `self.website` and not starts with '/'

        Examples:
            >>> from extract_emails.link_filters import DefaultLinkFilter
            >>> test_urls = ["https://example.com/page1.html","/page.html","/page.html", "https://google.com"]
            >>> link_filter = DefaultLinkFilter("https://example.com/")
            >>> filtered_urls = link_filter.filter(test_urls)
            >>> list(filtered_urls)
            ["https://example.com/page1.html", "https://example.com/page.html"]

        Args:
            links: List of links for filtering

        Returns:
            Set of filtered URLs
        """
        filtered_urls = set()
        for link in links:
            if link.startswith(self.website):
                filtered_urls.add(link)
            elif not link.startswith("http"):
                filtered_urls.add(urljoin(self.website, link))
        return filtered_urls
