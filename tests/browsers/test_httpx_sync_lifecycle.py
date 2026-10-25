from __future__ import annotations

import pytest

from extract_emails.browsers import HttpxBrowser, httpx_browser


class _Response:
    def __init__(self, text: str):
        self.text = text

    def raise_for_status(self) -> None:
        pass


class _Client:
    def __init__(
        self,
        text: str,
        fail_close: bool = False,
        enter_error: RuntimeError | None = None,
    ):
        self.text = text
        self.fail_close = fail_close
        self.enter_error = enter_error
        self.entered = False
        self.close_calls = 0
        self.get_calls = 0

    def __enter__(self):
        self.entered = True
        if self.enter_error is not None:
            raise self.enter_error
        return self

    def get(self, url: str) -> _Response:
        self.get_calls += 1
        return _Response(self.text)

    def close(self) -> None:
        self.close_calls += 1
        if self.fail_close:
            raise RuntimeError("close failed")


def test_httpx_sync_client_constructor_failure_can_be_retried(monkeypatch):
    startup_error = RuntimeError("constructor failed")
    client = _Client("retried client")
    constructor_calls = 0

    def make_client(**kwargs):
        nonlocal constructor_calls
        constructor_calls += 1
        if constructor_calls == 1:
            raise startup_error
        return client

    monkeypatch.setattr(httpx_browser.httpx, "Client", make_client)
    browser = HttpxBrowser()

    with pytest.raises(RuntimeError) as exc_info:
        browser.start()

    assert exc_info.value is startup_error
    browser.start()
    assert client.entered
    assert browser.get_page_source("https://example.test") == "retried client"
    assert client.get_calls == 1
    browser.stop()
    assert client.close_calls == 1


def test_httpx_sync_enter_failure_closes_acquired_client(monkeypatch):
    startup_error = RuntimeError("enter failed")
    client = _Client("unused", enter_error=startup_error)
    monkeypatch.setattr(httpx_browser.httpx, "Client", lambda **kwargs: client)
    browser = HttpxBrowser()

    with pytest.raises(RuntimeError) as exc_info:
        browser.start()

    assert exc_info.value is startup_error
    assert client.entered
    assert client.close_calls == 1


def test_httpx_sync_enter_and_close_failure_preserves_error_and_retries(monkeypatch):
    startup_error = RuntimeError("enter failed")
    failed_client = _Client("unused", fail_close=True, enter_error=startup_error)
    retry_client = _Client("retry succeeded")
    clients = iter((failed_client, retry_client))
    monkeypatch.setattr(httpx_browser.httpx, "Client", lambda **kwargs: next(clients))
    browser = HttpxBrowser()

    with pytest.raises(RuntimeError) as exc_info:
        browser.start()

    assert exc_info.value is startup_error
    assert failed_client.entered
    assert failed_client.close_calls == 1

    browser.start()
    assert retry_client.entered
    assert browser.get_page_source("https://example.test") == "retry succeeded"
    assert retry_client.get_calls == 1
    browser.stop()
    assert retry_client.close_calls == 1


def test_httpx_sync_close_failure_resets_state_and_allows_restart(monkeypatch):
    first_client = _Client("first", fail_close=True)
    second_client = _Client("second")
    clients = iter((first_client, second_client))
    monkeypatch.setattr(httpx_browser.httpx, "Client", lambda **kwargs: next(clients))
    browser = HttpxBrowser()
    browser.start()

    with pytest.raises(RuntimeError, match="close failed"):
        browser.stop()

    assert first_client.close_calls == 1
    browser.stop()
    assert first_client.close_calls == 1

    browser.start()
    assert second_client.entered
    assert browser.get_page_source("https://example.test") == "second"
    assert second_client.get_calls == 1
    browser.stop()
    assert second_client.close_calls == 1
