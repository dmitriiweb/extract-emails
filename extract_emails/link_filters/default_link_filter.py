from typing import List

from extract_emails.link_filters import LinkFilterInterface


class DefaultLinkFilter(LinkFilterInterface):
    """
    Default filter for links

    :param list(str) links: List of URLs
    """

    def filter(self, links: List[str]) -> List[str]:
        pass

