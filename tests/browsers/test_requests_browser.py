import pytest
import pytest_asyncio

from extract_emails.browsers import HttpxBrowser


@pytest.fixture
def browser():
    browser = HttpxBrowser()
    browser.start()
    try:
        yield browser
    finally:
        browser.stop()


@pytest_asyncio.fixture
async def async_browser():
    browser = HttpxBrowser()
    await browser.astart()
    try:
        yield browser
    finally:
        await browser.astop()


def test_get_page_source_returns_local_content(browser, local_http_server):
    page_source = browser.get_page_source(f"{local_http_server}/contacts")

    assert "Fixture content" in page_source
    assert "contact@example.test" in page_source


@pytest.mark.parametrize("path", ["/404", "/500"])
def test_get_page_source_returns_empty_for_http_errors(
    browser, local_http_server, path
):
    assert browser.get_page_source(f"{local_http_server}{path}") == ""


def test_get_page_source_follows_redirect(browser, local_http_server):
    page_source = browser.get_page_source(f"{local_http_server}/redirect")

    assert "Fixture content" in page_source


def test_get_page_source_preserves_empty_success(browser, local_http_server):
    assert browser.get_page_source(f"{local_http_server}/empty") == ""


def test_get_page_source_returns_empty_for_refused_connection(browser, refused_url):
    assert browser.get_page_source(refused_url) == ""


@pytest.mark.asyncio
async def test_aget_page_source_returns_local_content(async_browser, local_http_server):
    page_source = await async_browser.aget_page_source(f"{local_http_server}/contacts")

    assert "Fixture content" in page_source
    assert "contact@example.test" in page_source


@pytest.mark.parametrize("path", ["/404", "/500"])
@pytest.mark.asyncio
async def test_aget_page_source_returns_empty_for_http_errors(
    async_browser, local_http_server, path
):
    assert await async_browser.aget_page_source(f"{local_http_server}{path}") == ""


@pytest.mark.asyncio
async def test_aget_page_source_follows_redirect(async_browser, local_http_server):
    page_source = await async_browser.aget_page_source(f"{local_http_server}/redirect")

    assert "Fixture content" in page_source


@pytest.mark.asyncio
async def test_aget_page_source_preserves_empty_success(
    async_browser, local_http_server
):
    assert await async_browser.aget_page_source(f"{local_http_server}/empty") == ""


@pytest.mark.asyncio
async def test_aget_page_source_returns_empty_for_refused_connection(
    async_browser, refused_url
):
    assert await async_browser.aget_page_source(refused_url) == ""
