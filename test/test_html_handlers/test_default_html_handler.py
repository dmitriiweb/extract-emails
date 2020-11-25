import unittest

from extract_emails.html_handlers import DefaultHTMLHandler

HTML_EXAMPLE = """
<!doctype html>
<head>
<title>blah</title>
</head>
<body>
<p> blah blah example@example.com</p>
<p> blah blah example+example@example.co.uk</p>
<a href="example.com">link</a>
<a href="example2.com">link</a>
</body>
</html>
"""

HTML_EXAMPLE_NO_LINKS_NO_EMAILS = """
<!doctype html>
<head>
<title>blah</title>
</head>
<body>
<p> blah blah </p>
</body>
</html>
"""


class TestDefaultHTMLHandler(unittest.TestCase):
    def setUp(self) -> None:
        self.html_handler = DefaultHTMLHandler()
        self.html_handler_empty = DefaultHTMLHandler()

    def test_get_emails(self):
        emails = self.html_handler.get_emails(HTML_EXAMPLE)

        self.assertEqual(emails[0], "example@example.com")
        self.assertEqual(emails[1], "example+example@example.co.uk")

    def test_get_links(self):
        self.assertEqual(
            self.html_handler.get_links(HTML_EXAMPLE), ["example.com", "example2.com"]
        )

    def test_get_emails_empty(self):
        self.assertEqual(
            self.html_handler_empty.get_emails(HTML_EXAMPLE_NO_LINKS_NO_EMAILS), []
        )

    def test_get_links_empty(self):
        self.assertEqual(
            self.html_handler_empty.get_links(HTML_EXAMPLE_NO_LINKS_NO_EMAILS), []
        )


if __name__ == "__main__":
    unittest.main()
