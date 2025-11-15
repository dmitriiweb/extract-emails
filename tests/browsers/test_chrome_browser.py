import pytest
import pytest_asyncio

from extract_emails.browsers import ChromiumBrowser

@pytest_asyncio.fixture
async def browser():
    browser = ChromiumBrowser()
    await browser.astart()
    yield browser
    await browser.astop()

@pytest.mark.slow
async def test_get_page_source(browser):
    url = "https://en.wikipedia.org/wiki/Python_(programming_language)"
    page_source = await browser.aget_page_source(url)
    assert "Python (programming language)" in page_source

@pytest.mark.slow
async def test_get_page_source_wrong_url(browser):
    url = "ttps://en.wikipedia.org/wiki/Python_(programming_language)"
    page_source = await browser.aget_page_source(url)
    assert page_source == ""
