import typing

import httpx

from . import types
from .page_source_getter import PageSourceGetter


class HttpxGetter(PageSourceGetter):
    def __init__(self):
        self._client = httpx.AsyncClient()

    async def stop(self):
        await self._client.aclose()

    async def get_page_source(self, url: types.Url) -> types.HtmlPage:
        response = await self._client.get(url.url, headers=url.headers)
        return types.HtmlPage(url=url.url, source=response.text)
