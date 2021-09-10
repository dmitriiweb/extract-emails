import pytest

from extract_emails.browsers import ChromeBrowser


@pytest.fixture
def browser():
    browser = ChromeBrowser()
    browser.open()
    yield browser
    browser.close()


@pytest.mark.slow
def test_get_page_source(browser: ChromeBrowser):
    url = "https://en.wikipedia.org/wiki/Python_(programming_language)"
    page_source = browser.get_page_source(url)
    assert "Python (programming language)" in page_source


@pytest.mark.slow
def test_get_page_source_wrong_url(browser: ChromeBrowser):
    url = "ttps://en.wikipedia.org/wiki/Python_(programming_language)"
    page_source = browser.get_page_source(url)
    assert page_source == "<html><head></head><body></body></html>"
