from abc import ABC, abstractmethod
from typing import Iterable

from extract_emails.models import PageData


class DataSaver(ABC):
    def __init__(self, **kwargs):
        pass

    @abstractmethod
    def save(self, data: Iterable[PageData]):
        pass
