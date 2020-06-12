from typing import List
from abc import ABC, abstractmethod


class LinkFilterInterface(ABC):
    """
    Interface for link filters

    :param str website_address: website's address, e.g. https://example.com
    """

    def __init__(self, website_address: str):
        self.website = website_address

    @abstractmethod
    def filter(self, links: List[str]) -> List[str]:
        """
        Links filter

        :param list(str) links: List of URLs
        :return: Filtered list of URls
        """
        pass
