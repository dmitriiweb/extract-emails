import unittest

from extract_emails import EmailExtractor, Email
from extract_emails.browsers import ChromeBrowser


class TestEmailExtractor(unittest.TestCase):
    def test_email_extractor(self):
        url = "http://www.tomatinos.com/"
        emails = [
            Email("bakedincloverdale@gmail.com", url),
            Email("freshlybakedincloverdale@gmail.com", url),
        ]

        with ChromeBrowser() as browser:
            ee = EmailExtractor(url, browser, depth=2)
            e = ee.get_emails()
        self.assertEqual(e[0].as_dict(), emails[0].as_dict())
