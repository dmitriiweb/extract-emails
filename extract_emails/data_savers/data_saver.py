from abc import ABC, abstractmethod
from typing import Any, Iterable

from extract_emails.models import PageData


class DataSaver(ABC):
    def __init__(self, **kwargs: Any) -> None:
        """Accept legacy saver options without storing shared state.

        Args:
            kwargs: Legacy keyword arguments accepted for subclass compatibility.
        """
        super().__init__()

    @abstractmethod
    def save(self, data: Iterable[PageData]):
        pass
