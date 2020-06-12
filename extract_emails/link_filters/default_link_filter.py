from typing import List
from urllib.parse import urljoin

from extract_emails.link_filters import LinkFilterInterface


class DefaultLinkFilter(LinkFilterInterface):
    """
    Default filter for links

    :param list(str) links: List of URLs
    """

    checked_links = []

    def filter(self, links: List[str]) -> List[str]:
        filtered_urls = []
        for url in links:
            url = urljoin(self.website, url)
            if url.startswith(self.website) and url not in self.checked_links:
                self.checked_links.append(url)
                filtered_urls.append(url)
        return filtered_urls
