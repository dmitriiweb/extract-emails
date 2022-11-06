from abc import ABC
from abc import abstractmethod

from . import types


class PageSourceGetter(ABC):
    @abstractmethod
    async def stop(self):
        ...

    @abstractmethod
    async def get_page_source(self, url: types.Url) -> types.HtmlPage:
        ...
