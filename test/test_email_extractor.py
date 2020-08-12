import unittest

from extract_emails import EmailExtractor, Email
from extract_emails.browsers import ChromeBrowser


class TestEmailExtractor(unittest.TestCase):
    def test_email_extractor(self):
        browser = ChromeBrowser()
        browser.open()
        url = "http://www.tomatinos.com/"
        ee = EmailExtractor(url, browser, depth=2)
        emails = [
            Email("bakedincloverdale@gmail.com", url),
            Email("freshlybakedincloverdale@gmail.com", url),
        ]
        e = ee.get_emails()
        self.assertEqual(e[0].as_dict(), emails[0].as_dict())
