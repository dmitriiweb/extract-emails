import pytest

from extract_emails.browsers import HttpxBrowser


@pytest.fixture
def browser():
    browser = HttpxBrowser()
    browser.start()
    yield browser
    browser.stop()


@pytest.mark.slow
def test_get_page_source(browser):
    url = "https://en.wikipedia.org/wiki/Python_(programming_language)"
    page_source = browser.get_page_source(url)
    assert "Python (programming language)" in page_source


@pytest.mark.slow
def test_get_page_source_wrong_url(browser):
    url = "ttps://en.wikipedia.org/wiki/Python_(programming_language)"
    page_source = browser.get_page_source(url)
    assert page_source == ""
