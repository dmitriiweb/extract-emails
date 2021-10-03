from abc import ABC
from abc import abstractmethod
from typing import List
from typing import Type

from extract_emails.data_extractors import DataExtractor
from extract_emails.link_filters import LinkFilterBase


class IFactory(ABC):
    """Interface for factories"""

    @property
    @abstractmethod
    def link_filter(self) -> Type[LinkFilterBase]:
        """Initialize link filter"""

    @property
    @abstractmethod
    def data_extractors(self) -> List[Type[DataExtractor]]:
        """Initialize data extractors"""
