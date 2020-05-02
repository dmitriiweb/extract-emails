from abc import ABC, abstractmethod


class BrowserInterface(ABC):
    """Interface for browsers"""

    def __enter__(self):
        self.open()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def open(self):
        """Run a browser"""
        pass

    def close(self):
        """Close a browser"""

    @abstractmethod
    def get_page_source(self, url: str) -> str:
        """
        Return page source from url

        :param str url: page url
        :return: str, HTML from page
        """
