from __future__ import annotations

import httpx
from loguru import logger

from .page_source_getter import PageSourceGetter


class _SyncHttpxBrowser:
    client: httpx.Client

    def __init__(self, headers: dict[str, str] | None = None):
        super().__init__()
        self.headers = headers

    def start(self) -> None:
        self.client = httpx.Client(headers=self.headers, follow_redirects=True)
        self.client.__enter__()

    def stop(self) -> None:
        self.client.__exit__(None, None, None)

    def get_page_source(self, url: str) -> str:
        response = self.client.get(url)
        return response.text


class _AsyncHttpxBrowser:
    client: httpx.AsyncClient

    def __init__(self, headers: dict[str, str] | None = None):
        super().__init__()
        self.headers = headers

    async def start(self) -> None:
        self.client = httpx.AsyncClient(headers=self.headers, follow_redirects=True)
        await self.client.__aenter__()

    async def stop(self) -> None:
        await self.client.__aexit__(None, None, None)

    async def get_page_source(self, url: str) -> str:
        response = await self.client.get(url)
        return response.text


class HttpxBrowser(PageSourceGetter):
    headers: dict[str, str] | None
    _sync_browser: _SyncHttpxBrowser
    _async_browser: _AsyncHttpxBrowser

    def __init__(self, headers: dict[str, str] | None = None):
        super().__init__()
        if headers is None:
            headers = {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
        self.headers = headers

    def start(self) -> None:
        self._sync_browser = _SyncHttpxBrowser(self.headers)
        self._sync_browser.start()

    def stop(self) -> None:
        self._sync_browser.stop()

    def get_page_source(self, url: str) -> str:
        try:
            response = self._sync_browser.get_page_source(url)
        except Exception as e:
            logger.error(f"Could not get page source from {url}: {e}")
            return ""
        return response

    async def astart(self) -> None:
        self._async_browser = _AsyncHttpxBrowser(self.headers)
        await self._async_browser.start()

    async def astop(self) -> None:
        await self._async_browser.stop()

    async def aget_page_source(self, url: str) -> str:
        try:
            response = await self._async_browser.get_page_source(url)
        except Exception as e:
            logger.error(f"Could not get page source from {url}: {e}")
            return ""
        return response
