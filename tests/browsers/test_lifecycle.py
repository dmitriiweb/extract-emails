from __future__ import annotations

import asyncio

import httpx
import pytest

from extract_emails.browsers import (
    ChromiumBrowser,
    HttpxBrowser,
    chromium_browser,
    httpx_browser,
)


class _Resource:
    def __init__(self, fail_close: bool = False):
        self.closed = 0
        self.fail_close = fail_close

    def close(self):
        self.closed += 1
        if self.fail_close:
            raise ValueError("close failed")

    def stop(self):
        self.close()

    def launch(self, **kwargs):
        return _Resource()

    def new_context(self, **kwargs):
        return _Resource()

    def new_page(self):
        return _Resource()


class _AsyncResource(_Resource):
    async def close(self):
        self.closed += 1
        if self.fail_close:
            raise ValueError("close failed")

    async def stop(self):
        await self.close()

    async def launch(self, **kwargs):
        return _AsyncResource()

    async def new_context(self, **kwargs):
        return _AsyncResource()

    async def new_page(self):
        return _AsyncResource()


def test_httpx_sync_lifecycle_and_errors(monkeypatch):
    class Client:
        def __init__(self, **kwargs):
            self.closed = 0

        def __enter__(self):
            return self

        def close(self):
            self.closed += 1

        def get(self, url):
            raise RuntimeError("implementation bug")

    monkeypatch.setattr(httpx_browser.httpx, "Client", Client)
    browser = HttpxBrowser()
    browser.stop()
    browser.start()
    with pytest.raises(RuntimeError, match="already started"):
        browser.start()
    with pytest.raises(RuntimeError, match="implementation bug"):
        browser.get_page_source("https://example.com")
    browser.stop()
    browser.stop()
    browser.start()
    browser.stop()


def test_httpx_async_status_errors_return_empty_string(monkeypatch):
    class Client:
        def __init__(self, **kwargs):
            pass

        async def __aenter__(self):
            return self

        async def aclose(self):
            pass

        async def get(self, url):
            request = httpx.Request("GET", url)
            return httpx.Response(404, request=request)

    monkeypatch.setattr(httpx_browser.httpx, "AsyncClient", Client)
    browser = HttpxBrowser()

    async def exercise():
        await browser.astart()
        assert await browser.aget_page_source("https://example.com") == ""
        await browser.astop()

    asyncio.run(exercise())


def test_chromium_expected_navigation_errors_return_empty(monkeypatch):
    failure = chromium_browser.PlaywrightError("navigation failed")
    browser = ChromiumBrowser()
    browser._sync_browser = type(
        "Fake",
        (),
        {
            "playwright": object(),
            "get_page_source": lambda self, url: (_ for _ in ()).throw(failure),
        },
    )()
    assert browser.get_page_source("https://example.com") == ""

    async def fail_navigation(self, url):
        raise failure

    browser._async_browser = type(
        "FakeAsync",
        (),
        {"playwright": object(), "get_page_source": fail_navigation},
    )()

    async def exercise():
        assert await browser.aget_page_source("https://example.com") == ""

    asyncio.run(exercise())


def test_httpx_async_lifecycle_and_errors(monkeypatch):
    class Client:
        def __init__(self, **kwargs):
            self.closed = 0

        async def __aenter__(self):
            return self

        async def aclose(self):
            self.closed += 1

        async def get(self, url):
            raise RuntimeError("implementation bug")

    monkeypatch.setattr(httpx_browser.httpx, "AsyncClient", Client)
    browser = HttpxBrowser()

    async def exercise():
        await browser.astop()
        await browser.astart()
        with pytest.raises(RuntimeError, match="already started"):
            await browser.astart()
        with pytest.raises(RuntimeError, match="implementation bug"):
            await browser.aget_page_source("https://example.com")
        await browser.astop()
        await browser.astop()
        await browser.astart()
        await browser.astop()

    asyncio.run(exercise())


def test_httpx_status_errors_return_empty_string(monkeypatch):
    class Client:
        def __init__(self, **kwargs):
            pass

        def __enter__(self):
            return self

        def close(self):
            pass

        def get(self, url):
            request = httpx.Request("GET", url)
            return httpx.Response(404, request=request)

    monkeypatch.setattr(httpx_browser.httpx, "Client", Client)
    browser = HttpxBrowser()
    browser.start()
    assert browser.get_page_source("https://example.com") == ""
    browser.stop()


@pytest.mark.parametrize("failure_step", ["start", "launch", "context", "page"])
def test_chromium_sync_partial_startup_rolls_back(monkeypatch, failure_step):
    resources = []

    class Fake(_Resource):
        def __init__(self, step=None):
            super().__init__()
            self.step = step
            resources.append(self)
            self.chromium = self

        def start(self):
            if failure_step == "start":
                raise RuntimeError("startup failed")
            return self

        def launch(self, **kwargs):
            if failure_step == "launch":
                raise RuntimeError("startup failed")
            return Fake("browser")

        def new_context(self, **kwargs):
            if failure_step == "context":
                raise RuntimeError("startup failed")
            return Fake("context")

        def new_page(self):
            if failure_step == "page":
                raise RuntimeError("startup failed")
            return Fake("page")

    monkeypatch.setattr(chromium_browser, "sync_playwright", lambda: Fake())
    browser = ChromiumBrowser()
    with pytest.raises(RuntimeError, match="startup failed"):
        browser.start()
    acquired = ["start", "launch", "context", "page"].index(failure_step)
    assert [resource.closed for resource in resources] == [1] * acquired + [0] * (
        len(resources) - acquired
    )


def test_chromium_sync_cleanup_continues_and_restart(monkeypatch):
    created = []
    fail_next_context_close = True

    class Fake(_Resource):
        def __init__(self, fail_close=False):
            super().__init__(fail_close)
            self.chromium = self
            created.append(self)

        def start(self):
            return self

        def launch(self, **kwargs):
            return Fake()

        def new_context(self, **kwargs):
            nonlocal fail_next_context_close
            fail_close = fail_next_context_close
            fail_next_context_close = False
            return Fake(fail_close=fail_close)

        def new_page(self):
            return Fake()

    monkeypatch.setattr(chromium_browser, "sync_playwright", lambda: Fake())
    browser = ChromiumBrowser()
    browser.stop()
    browser.start()
    with pytest.raises(RuntimeError, match="already started"):
        browser.start()
    with pytest.raises(ValueError, match="close failed"):
        browser.stop()
    assert [resource.closed for resource in created] == [1, 1, 1, 1]
    browser.stop()
    assert [resource.closed for resource in created] == [1, 1, 1, 1]
    browser.start()
    browser.stop()
    assert [resource.closed for resource in created] == [1] * 8


def test_chromium_async_lifecycle(monkeypatch):
    created = []

    class Fake(_AsyncResource):
        def __init__(self):
            super().__init__()
            self.chromium = self
            created.append(self)

        async def start(self):
            return self

        async def launch(self, **kwargs):
            return Fake()

        async def new_context(self, **kwargs):
            return Fake()

        async def new_page(self):
            return Fake()

    monkeypatch.setattr(chromium_browser, "async_playwright", lambda: Fake())
    browser = ChromiumBrowser()

    async def exercise():
        await browser.astop()
        await browser.astart()
        with pytest.raises(RuntimeError, match="already started"):
            await browser.astart()
        await browser.astop()
        await browser.astop()
        await browser.astart()
        await browser.astop()

    asyncio.run(exercise())
    assert all(resource.closed == 1 for resource in created)


def test_chromium_unexpected_errors_propagate(monkeypatch):
    browser = ChromiumBrowser()
    browser._sync_browser = type(
        "Fake",
        (),
        {
            "playwright": object(),
            "get_page_source": lambda self, url: (_ for _ in ()).throw(
                RuntimeError("bug")
            ),
        },
    )()
    with pytest.raises(RuntimeError, match="bug"):
        browser.get_page_source("https://example.com")


@pytest.mark.parametrize("failure_step", ["start", "launch", "context", "page"])
def test_chromium_async_partial_startup_rolls_back(monkeypatch, failure_step):
    resources = []

    class Fake(_AsyncResource):
        def __init__(self, kind="playwright"):
            super().__init__()
            self.kind = kind
            self.chromium = self
            resources.append(self)

        async def start(self):
            if failure_step == "start":
                raise RuntimeError("startup failed")
            return self

        async def launch(self, **kwargs):
            if failure_step == "launch":
                raise RuntimeError("startup failed")
            return Fake("browser")

        async def new_context(self, **kwargs):
            if failure_step == "context":
                raise RuntimeError("startup failed")
            return Fake("context")

        async def new_page(self):
            if failure_step == "page":
                raise RuntimeError("startup failed")
            return Fake("page")

    monkeypatch.setattr(chromium_browser, "async_playwright", lambda: Fake())
    browser = ChromiumBrowser()

    async def exercise():
        with pytest.raises(RuntimeError, match="startup failed"):
            await browser.astart()

    asyncio.run(exercise())
    acquired = ["start", "launch", "context", "page"].index(failure_step)
    assert [resource.closed for resource in resources] == [1] * acquired + [0] * (
        len(resources) - acquired
    )


def test_chromium_async_cleanup_continues_and_restarts(monkeypatch):
    created = []
    fail_next_context_close = True

    class Fake(_AsyncResource):
        def __init__(self, fail_close=False):
            super().__init__(fail_close)
            self.chromium = self
            created.append(self)

        async def start(self):
            return self

        async def launch(self, **kwargs):
            return Fake()

        async def new_context(self, **kwargs):
            nonlocal fail_next_context_close
            fail_close = fail_next_context_close
            fail_next_context_close = False
            return Fake(fail_close=fail_close)

        async def new_page(self):
            return Fake()

    monkeypatch.setattr(chromium_browser, "async_playwright", lambda: Fake())
    browser = ChromiumBrowser()

    async def exercise():
        await browser.astop()
        await browser.astart()
        with pytest.raises(RuntimeError, match="already started"):
            await browser.astart()
        with pytest.raises(ValueError, match="close failed"):
            await browser.astop()
        assert [resource.closed for resource in created] == [1, 1, 1, 1]
        await browser.astop()
        assert [resource.closed for resource in created] == [1, 1, 1, 1]
        await browser.astart()
        await browser.astop()
        assert [resource.closed for resource in created] == [1] * 8

    asyncio.run(exercise())


def test_lazy_export_reports_only_missing_backend_dependency(monkeypatch):
    import extract_emails.browsers as browsers

    def missing_backend(*args, **kwargs):
        raise ModuleNotFoundError("No module named 'playwright'", name="playwright")

    monkeypatch.setattr(browsers, "import_module", missing_backend)
    with pytest.raises(ImportError, match=r"extract-emails\[playwright\]"):
        browsers.__getattr__("ChromiumBrowser")

    def unrelated_missing_module(*args, **kwargs):
        raise ModuleNotFoundError("No module named 'unrelated'", name="unrelated")

    monkeypatch.setattr(browsers, "import_module", unrelated_missing_module)
    with pytest.raises(ModuleNotFoundError, match="unrelated"):
        browsers.__getattr__("HttpxBrowser")
