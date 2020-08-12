import unittest

from extract_emails import EmailExtractor
from extract_emails.browsers import ChromeBrowser


class TestEmailExtractor(unittest.TestCase):
    def test_email_extractor(self):
        browser = ChromeBrowser()
        browser.open()
        url = "http://www.tomatinos.com/"
        ee = EmailExtractor(url, browser)
        emails = ["bakedincloverdale@gmail.com", "freshlybakedincloverdale@gmail.com"]
        self.assertEqual(ee.get_emails(), emails)
        browser.close()
