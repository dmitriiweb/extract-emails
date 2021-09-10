import pytest

from extract_emails.browsers import RequestsBrowser


@pytest.fixture
def browser():
    return RequestsBrowser()


@pytest.mark.slow
def test_get_page_source(browser: RequestsBrowser):
    url = "https://en.wikipedia.org/wiki/Python_(programming_language)"
    page_source = browser.get_page_source(url)
    assert "Python (programming language)" in page_source


@pytest.mark.slow
def test_get_page_source_wrong_url(browser: RequestsBrowser):
    url = "ttps://en.wikipedia.org/wiki/Python_(programming_language)"
    page_source = browser.get_page_source(url)

    assert page_source == ""
