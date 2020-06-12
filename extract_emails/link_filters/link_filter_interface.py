from typing import List
from abc import ABC, abstractmethod


class LinkFilterInterface(ABC):
    """
    Interface for link filters

    :param list(str) links: List of URLs
    """

    def __init__(self, links: List[str]):
        self.links = links

    @abstractmethod
    def filter(self) -> List[str]:
        """
        Links filter

        :return: Filtered list of URls
        """
        pass
