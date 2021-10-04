import pytest

from extract_emails.browsers.chrome_browser import ChromeBrowser


@pytest.mark.slow
def test_get_page_source():
    browser = ChromeBrowser()
    browser.open()
    url = "https://en.wikipedia.org/wiki/Python_(programming_language)"
    page_source = browser.get_page_source(url)
    assert "Python (programming language)" in page_source
    browser.close()


@pytest.mark.slow
def test_get_page_source_wrong_url():
    with ChromeBrowser() as browser:
        url = "ttps://en.wikipedia.org/wiki/Python_(programming_language)"
        page_source = browser.get_page_source(url)

    assert page_source == "<html><head></head><body></body></html>"
