from __future__ import annotations

from loguru import logger
from playwright.async_api import Browser as AsyncBrowser
from playwright.async_api import BrowserContext as AsyncBrowserContext
from playwright.async_api import Page as AsyncPage
from playwright.async_api import async_playwright
from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright

from .page_source_getter import PageSourceGetter


class _SyncChromiumBrowser:
    browser: Browser
    context: BrowserContext
    page: Page

    def __init__(self, headers: dict[str, str] | None = None, headless: bool = True):
        super().__init__()
        self.headers = headers
        self.headless = headless
        self.playwright = None

    def start(self) -> None:
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=self.headless)
        self.context = self.browser.new_context(
            extra_http_headers=self.headers if self.headers else {}
        )
        self.page = self.context.new_page()

    def stop(self) -> None:
        if hasattr(self, "page"):
            self.page.close()
        if hasattr(self, "context"):
            self.context.close()
        if hasattr(self, "browser"):
            self.browser.close()
        if self.playwright:
            self.playwright.stop()

    def get_page_source(self, url: str) -> str:
        self.page.goto(url)
        # Wait for the page to be fully loaded
        self.page.wait_for_load_state("networkidle")
        return self.page.content()


class _AsyncChromiumBrowser:
    browser: AsyncBrowser
    context: AsyncBrowserContext
    page: AsyncPage

    def __init__(self, headers: dict[str, str] | None = None, headless: bool = True):
        super().__init__()
        self.headers = headers
        self.headless = headless
        self.playwright = None

    async def start(self) -> None:
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=self.headless)
        self.context = await self.browser.new_context(
            extra_http_headers=self.headers if self.headers else {}
        )
        self.page = await self.context.new_page()

    async def stop(self) -> None:
        if hasattr(self, "page"):
            await self.page.close()
        if hasattr(self, "context"):
            await self.context.close()
        if hasattr(self, "browser"):
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()

    async def get_page_source(self, url: str) -> str:
        await self.page.goto(url)
        # Wait for the page to be fully loaded
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
        self._sync_browser = _SyncChromiumBrowser(self.headers, self.headless)
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
        self._async_browser = _AsyncChromiumBrowser(self.headers, self.headless)
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
