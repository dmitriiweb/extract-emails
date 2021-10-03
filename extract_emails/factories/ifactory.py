from abc import ABC
from abc import abstractmethod
from typing import List
from typing import Type

from extract_emails.data_extractors import DataExtractor
from extract_emails.link_filters import LinkFilterBase


class IFactory(ABC):
    @property
    @abstractmethod
    def link_filter(self) -> Type[LinkFilterBase]:
        pass

    @property
    @abstractmethod
    def data_extractors(self) -> List[Type[DataExtractor]]:
        pass
