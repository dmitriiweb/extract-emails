from __future__ import annotations

import httpx
from loguru import logger

from .page_source_getter import PageSourceGetter


class _SyncHttpxBrowser:
    client: httpx.Client | None

    def __init__(self, headers: dict[str, str] | None = None):
        super().__init__()
        self.headers = headers
        self.client = None

    def start(self) -> None:
        if self.client is not None:
            raise RuntimeError("HTTPX browser is already started")
        client = httpx.Client(headers=self.headers, follow_redirects=True)
        try:
            client.__enter__()
        except BaseException:
            try:
                client.close()
            except BaseException:
                pass
            raise
        self.client = client

    def stop(self) -> None:
        client, self.client = self.client, None
        if client is not None:
            client.close()

    def get_page_source(self, url: str) -> str:
        if self.client is None:
            raise RuntimeError("HTTPX browser is not started")
        response = self.client.get(url)
        response.raise_for_status()
        return response.text


class _AsyncHttpxBrowser:
    client: httpx.AsyncClient | None

    def __init__(self, headers: dict[str, str] | None = None):
        super().__init__()
        self.headers = headers
        self.client = None

    async def start(self) -> None:
        if self.client is not None:
            raise RuntimeError("HTTPX browser is already started")
        client = httpx.AsyncClient(headers=self.headers, follow_redirects=True)
        try:
            await client.__aenter__()
        except BaseException:
            try:
                await client.aclose()
            except BaseException:
                pass
            raise
        self.client = client

    async def stop(self) -> None:
        client, self.client = self.client, None
        if client is not None:
            await client.aclose()

    async def get_page_source(self, url: str) -> str:
        if self.client is None:
            raise RuntimeError("HTTPX browser is not started")
        response = await self.client.get(url)
        response.raise_for_status()
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
        if hasattr(self, "_sync_browser") and self._sync_browser.client is not None:
            raise RuntimeError("HTTPX browser is already started")
        self._sync_browser = _SyncHttpxBrowser(self.headers)
        self._sync_browser.start()

    def stop(self) -> None:
        if hasattr(self, "_sync_browser"):
            self._sync_browser.stop()

    def get_page_source(self, url: str) -> str:
        try:
            return self._sync_browser.get_page_source(url)
        except httpx.HTTPError as e:
            logger.error(f"Could not get page source from {url}: {e}")
            return ""

    async def astart(self) -> None:
        if hasattr(self, "_async_browser") and self._async_browser.client is not None:
            raise RuntimeError("HTTPX browser is already started")
        self._async_browser = _AsyncHttpxBrowser(self.headers)
        await self._async_browser.start()

    async def astop(self) -> None:
        if hasattr(self, "_async_browser"):
            await self._async_browser.stop()

    async def aget_page_source(self, url: str) -> str:
        try:
            return await self._async_browser.get_page_source(url)
        except httpx.HTTPError as e:
            logger.error(f"Could not get page source from {url}: {e}")
            return ""
