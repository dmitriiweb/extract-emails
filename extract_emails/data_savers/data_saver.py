from abc import ABC
from abc import abstractmethod

from extract_emails.models import PageData


class DataSaver(ABC):
    def __init__(self, **kwargs):
        pass

    @abstractmethod
    def save(self, data: PageData):
        pass
