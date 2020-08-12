import unittest

from extract_emails import Email

EMAIL = "example@example.com"
PAGE_SOURCE = "https://example.com"


class TestEmail(unittest.TestCase):
    def setUp(self):
        self.email = Email(email=EMAIL, source_page=PAGE_SOURCE)

    def test_as_dict(self):
        as_dict = {"email": EMAIL, "source_page": PAGE_SOURCE}
        self.assertEqual(self.email.as_dict(), as_dict)

    def test_as_list(self):
        as_list = [EMAIL, PAGE_SOURCE]
        self.assertEqual(self.email.as_list(), as_list)
