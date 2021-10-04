from abc import ABC
from abc import abstractmethod


class PageSourceGetter(ABC):
    """All browsers must inherit from this class"""

    @abstractmethod
    def get_page_source(self, url: str) -> str:
        """Return page content from an URL

        Args:
            url: URL

        Returns:
            page content (html, json, whatever)
        """
