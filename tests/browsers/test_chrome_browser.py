import pytest
import pytest_asyncio

from extract_emails.browsers import ChromiumBrowser


@pytest.fixture
def browser():
    browser = ChromiumBrowser()
    browser.start()
    try:
        yield browser
    finally:
        browser.stop()


@pytest_asyncio.fixture
async def async_browser():
    browser = ChromiumBrowser()
    await browser.astart()
    try:
        yield browser
    finally:
        await browser.astop()


@pytest.mark.slow
def test_get_page_source_returns_local_content(browser, local_http_server):
    page_source = browser.get_page_source(f"{local_http_server}/contacts")

    assert "Fixture content" in page_source
    assert "contact@example.test" in page_source


@pytest.mark.slow
def test_get_page_source_follows_redirect(browser, local_http_server):
    page_source = browser.get_page_source(f"{local_http_server}/redirect")

    assert "Fixture content" in page_source


@pytest.mark.slow
def test_get_page_source_preserves_empty_success(browser, local_http_server):
    page_source = browser.get_page_source(f"{local_http_server}/empty")

    assert "<body" in page_source
    assert "Fixture content" not in page_source


@pytest.mark.parametrize(
    ("path", "expected"),
    [("/404", "Not found fixture"), ("/500", "Server error fixture")],
)
@pytest.mark.slow
def test_get_page_source_preserves_http_error_page(
    browser, local_http_server, path, expected
):
    assert expected in browser.get_page_source(f"{local_http_server}{path}")


@pytest.mark.slow
@pytest.mark.asyncio
async def test_aget_page_source_returns_local_content(async_browser, local_http_server):
    page_source = await async_browser.aget_page_source(f"{local_http_server}/contacts")

    assert "Fixture content" in page_source
    assert "contact@example.test" in page_source


@pytest.mark.slow
@pytest.mark.asyncio
async def test_aget_page_source_follows_redirect(async_browser, local_http_server):
    page_source = await async_browser.aget_page_source(f"{local_http_server}/redirect")

    assert "Fixture content" in page_source


@pytest.mark.slow
@pytest.mark.asyncio
async def test_aget_page_source_preserves_empty_success(
    async_browser, local_http_server
):
    page_source = await async_browser.aget_page_source(f"{local_http_server}/empty")

    assert "<body" in page_source
    assert "Fixture content" not in page_source


@pytest.mark.parametrize(
    ("path", "expected"),
    [("/404", "Not found fixture"), ("/500", "Server error fixture")],
)
@pytest.mark.slow
@pytest.mark.asyncio
async def test_aget_page_source_preserves_http_error_page(
    async_browser, local_http_server, path, expected
):
    page_source = await async_browser.aget_page_source(f"{local_http_server}{path}")

    assert expected in page_source


@pytest.mark.slow
def test_get_page_source_returns_empty_for_refused_connection(browser, refused_url):
    assert browser.get_page_source(refused_url) == ""


@pytest.mark.slow
@pytest.mark.asyncio
async def test_aget_page_source_returns_empty_for_refused_connection(
    async_browser, refused_url
):
    assert await async_browser.aget_page_source(refused_url) == ""
