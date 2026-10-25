from __future__ import annotations

from loguru import logger
from playwright.async_api import Browser as AsyncBrowser
from playwright.async_api import BrowserContext as AsyncBrowserContext
from playwright.async_api import Page as AsyncPage
from playwright.async_api import async_playwright
from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright
from playwright.sync_api import Error as PlaywrightError

from .page_source_getter import PageSourceGetter


class _SyncChromiumBrowser:
    browser: Browser | None
    context: BrowserContext | None
    page: Page | None

    def __init__(self, headers: dict[str, str] | None = None, headless: bool = True):
        super().__init__()
        self.headers = headers
        self.headless = headless
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    def start(self) -> None:
        if self.playwright is not None:
            raise RuntimeError("Chromium browser is already started")
        try:
            self.playwright = sync_playwright().start()  # type: ignore
            self.browser = self.playwright.chromium.launch(headless=self.headless)  # type: ignore
            self.context = self.browser.new_context(
                extra_http_headers=self.headers if self.headers else {}
            )
            self.page = self.context.new_page()
        except BaseException:
            try:
                self._close_resources()
            except BaseException:
                pass
            raise

    def _close_resources(self) -> None:
        error = None
        for resource, close in (
            ("page", "close"),
            ("context", "close"),
            ("browser", "close"),
            ("playwright", "stop"),
        ):
            instance = getattr(self, resource)
            setattr(self, resource, None)
            if instance is not None:
                try:
                    getattr(instance, close)()
                except BaseException as exc:
                    if error is None:
                        error = exc
        if error is not None:
            raise error

    def stop(self) -> None:
        self._close_resources()

    def get_page_source(self, url: str) -> str:
        if self.page is None:
            raise RuntimeError("Chromium browser is not started")
        self.page.goto(url)
        self.page.wait_for_load_state("networkidle")
        return self.page.content()


class _AsyncChromiumBrowser:
    browser: AsyncBrowser | None
    context: AsyncBrowserContext | None
    page: AsyncPage | None

    def __init__(self, headers: dict[str, str] | None = None, headless: bool = True):
        super().__init__()
        self.headers = headers
        self.headless = headless
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    async def start(self) -> None:
        if self.playwright is not None:
            raise RuntimeError("Chromium browser is already started")
        try:
            self.playwright = await async_playwright().start()  # type: ignore
            self.browser = await self.playwright.chromium.launch(headless=self.headless)  # type: ignore
            self.context = await self.browser.new_context(
                extra_http_headers=self.headers if self.headers else {}
            )
            self.page = await self.context.new_page()
        except BaseException:
            try:
                await self._close_resources()
            except BaseException:
                pass
            raise

    async def _close_resources(self) -> None:
        error = None
        for resource, close in (
            ("page", "close"),
            ("context", "close"),
            ("browser", "close"),
            ("playwright", "stop"),
        ):
            instance = getattr(self, resource)
            setattr(self, resource, None)
            if instance is not None:
                try:
                    await getattr(instance, close)()
                except BaseException as exc:
                    if error is None:
                        error = exc
        if error is not None:
            raise error

    async def stop(self) -> None:
        await self._close_resources()

    async def get_page_source(self, url: str) -> str:
        if self.page is None:
            raise RuntimeError("Chromium browser is not started")
        await self.page.goto(url)
        await self.page.wait_for_load_state("networkidle")
        return await self.page.content()


class ChromiumBrowser(PageSourceGetter):
    headers: dict[str, str] | None
    headless: bool
    _sync_browser: _SyncChromiumBrowser
    _async_browser: _AsyncChromiumBrowser

    def __init__(self, headers: dict[str, str] | None = None, headless: bool = True):
        self.headers = headers
        self.headless = headless

    def start(self) -> None:
        if hasattr(self, "_sync_browser") and self._sync_browser.playwright is not None:
            raise RuntimeError("Chromium browser is already started")
        self._sync_browser = _SyncChromiumBrowser(self.headers, self.headless)
        self._sync_browser.start()

    def stop(self) -> None:
        if hasattr(self, "_sync_browser"):
            self._sync_browser.stop()

    def get_page_source(self, url: str) -> str:
        try:
            return self._sync_browser.get_page_source(url)
        except PlaywrightError as e:
            logger.error(f"Could not get page source from {url}: {e}")
            return ""

    async def astart(self) -> None:
        if (
            hasattr(self, "_async_browser")
            and self._async_browser.playwright is not None
        ):
            raise RuntimeError("Chromium browser is already started")
        self._async_browser = _AsyncChromiumBrowser(self.headers, self.headless)
        await self._async_browser.start()

    async def astop(self) -> None:
        if hasattr(self, "_async_browser"):
            await self._async_browser.stop()

    async def aget_page_source(self, url: str) -> str:
        try:
            return await self._async_browser.get_page_source(url)
        except PlaywrightError as e:
            logger.error(f"Could not get page source from {url}: {e}")
            return ""
