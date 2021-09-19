from abc import ABC
from abc import abstractmethod
from typing import List

from extract_emails.models import PageData


class DataExtractor(ABC):
    """Base class for all data extractors"""

    @abstractmethod
    def get_data(self, page_source: str) -> List[str]:
        """Extract needed data from a string

        Args:
            page_source: webpage content

        Returns:
            List of data, e.g. ['email@email.com', 'email2@email.com']
        """
        pass
