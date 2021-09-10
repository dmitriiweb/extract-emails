from abc import ABC
from abc import abstractmethod


"""
browser = ChromeBrowser()
data_extractor1 = EmailExtractor()
data_extractor2 = LinkedInExtractor()
browser.run()

data_getter = DataGetter(browser, [data_extractor1, data_extractor2], urls=[])
data = data_getter.get_data()

browser.close()
"""


class BrowserInterface(ABC):
    """
    BrowserInterface
    -----------------
    Interface for browsers
    """

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @abstractmethod
    def close(self):
        """Close a browser"""

    @abstractmethod
    def get_page_source(self, url: str) -> str:
        """
        Return page source from url

        :param str url: page url
        :return: str, HTML from page
        """
