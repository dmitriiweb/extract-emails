from __future__ import annotations

import pytest

from extract_emails.browsers import HttpxBrowser


async def test_httpx_async_constructor_failure_preserves_error_and_allows_retry(
    monkeypatch,
):
    failure = RuntimeError("constructor failed")
    clients = []
    attempts = 0

    class Client:
        def __init__(self, **kwargs):
            nonlocal attempts
            attempts += 1
            if attempts == 1:
                raise failure
            self.closed = False
            clients.append(self)

        async def __aenter__(self):
            return self

        async def aclose(self):
            self.closed = True

    monkeypatch.setattr(
        "extract_emails.browsers.httpx_browser.httpx.AsyncClient", Client
    )
    browser = HttpxBrowser()

    with pytest.raises(RuntimeError) as raised:
        await browser.astart()
    assert raised.value is failure

    await browser.astart()
    assert len(clients) == 1
    client = clients[0]
    await browser.astop()
    assert client.closed


async def test_httpx_async_enter_failure_closes_instance_and_allows_retry(monkeypatch):
    failure = RuntimeError("enter failed")
    clients = []

    class Client:
        def __init__(self, **kwargs):
            self.closed = False
            self.entered = False
            clients.append(self)

        async def __aenter__(self):
            if len(clients) == 1:
                raise failure
            self.entered = True
            return self

        async def aclose(self):
            self.closed = True

    monkeypatch.setattr(
        "extract_emails.browsers.httpx_browser.httpx.AsyncClient", Client
    )
    browser = HttpxBrowser()

    with pytest.raises(RuntimeError) as raised:
        await browser.astart()
    assert raised.value is failure
    failed_client = clients[0]
    assert failed_client.closed

    await browser.astart()
    active_client = clients[1]
    assert active_client.entered
    await browser.astop()
    assert active_client.closed


async def test_httpx_async_enter_and_close_failures_preserve_start_error_and_retry(
    monkeypatch,
):
    startup_failure = RuntimeError("enter failed")
    close_failure = RuntimeError("close failed")
    clients = []

    class Client:
        def __init__(self, **kwargs):
            self.closed = False
            self.close_attempts = 0
            self.entered = False
            clients.append(self)

        async def __aenter__(self):
            if len(clients) == 1:
                raise startup_failure
            self.entered = True
            return self

        async def aclose(self):
            self.close_attempts += 1
            if not self.entered:
                raise close_failure
            self.closed = True

    monkeypatch.setattr(
        "extract_emails.browsers.httpx_browser.httpx.AsyncClient", Client
    )
    browser = HttpxBrowser()

    with pytest.raises(RuntimeError) as raised:
        await browser.astart()
    assert raised.value is startup_failure
    failed_client = clients[0]
    assert failed_client.close_attempts == 1
    await browser.astart()
    active_client = clients[1]
    assert active_client.entered
    await browser.astop()
    assert active_client.closed
    assert failed_client is not active_client


async def test_httpx_async_close_failure_resets_state_and_allows_restart(monkeypatch):
    clients = []

    class Client:
        def __init__(self, **kwargs):
            self.closed = False
            self.close_attempts = 0
            clients.append(self)

        async def __aenter__(self):
            return self

        async def aclose(self):
            self.close_attempts += 1
            if self is clients[0]:
                raise RuntimeError("close failed")
            self.closed = True

    monkeypatch.setattr(
        "extract_emails.browsers.httpx_browser.httpx.AsyncClient", Client
    )
    browser = HttpxBrowser()
    await browser.astart()
    first_client = clients[0]

    with pytest.raises(RuntimeError, match="close failed"):
        await browser.astop()
    with pytest.raises(RuntimeError):
        await browser.aget_page_source("https://example.com")

    await browser.astop()
    assert first_client.close_attempts == 1

    await browser.astart()
    second_client = clients[1]
    assert second_client is not first_client
    await browser.astop()
    assert second_client.closed
