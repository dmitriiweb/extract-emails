from abc import ABC
from abc import abstractmethod
from typing import Set


class DataExtractor(ABC):
    """Base class for all data extractors"""

    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the data extractor, e.g. email, linkedin"""

    @abstractmethod
    def get_data(self, page_source: str) -> Set[str]:
        """Extract needed data from a string

        Args:
            page_source: webpage content

        Returns:
            Set of data, e.g. {'email@email.com', 'email2@email.com'}
        """
