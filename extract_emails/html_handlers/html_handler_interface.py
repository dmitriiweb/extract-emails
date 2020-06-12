from typing import List
from abc import ABC, abstractmethod


class HTMLHandlerInterface(ABC):
    """
    Interface for HTML handlers

    :param str page_source: HTML page source
    """

    def __init__(self, page_source: str):
        self.page_source = page_source

    @abstractmethod
    def get_emails(self) -> List[str]:
        """
        Extract all sequences similar to email

        :return: list(str), ['example@gmail.com', 'example@example.com', ...]
        """
        pass

    @abstractmethod
    def get_links(self) -> List[str]:
        """
        Extract all URLs corresponding to current website

        :return: list(str)
        """
        pass
