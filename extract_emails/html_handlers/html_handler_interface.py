from typing import List
from abc import ABC, abstractmethod


class HTMLHandlerInterface(ABC):
    """
    Interface for HTML handlers
    """

    @abstractmethod
    def get_emails(self, page_source: str) -> List[str]:
        """
        Extract all sequences similar to email

        :param str page_source: HTML page source
        :return: list(str), ['example@gmail.com', 'example@example.com', ...]
        """
        pass

    @abstractmethod
    def get_links(self, page_source: str) -> List[str]:
        """
        Extract all URLs corresponding to current website

        :param str page_source: HTML page source
        :return: list(str)
        """
        pass
