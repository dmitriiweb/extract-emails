import unittest

from extract_emails.browsers import ChromeBrowser


class TestChromeBrowser(unittest.TestCase):
    def setUp(self) -> None:
        self.browser = ChromeBrowser()

    def tearDown(self) -> None:
        self.browser.close()

    def test_get_page_source(self):
        url = "https://en.wikipedia.org/wiki/Python_(programming_language)"
        page_source = self.browser.get_page_source(url)
        self.assertIn("Python (programming language)", page_source)

    def test_get_page_source_wrong_url(self):
        url = "ttps://en.wikipedia.org/wiki/Python_(programming_language)"
        page_source = self.browser.get_page_source(url)
        self.assertIn("", page_source)
