import unittest

from extract_emails.html_handlers import DefaultHTMLHandler

HTML_EXAMPLE = '''
<!doctype html>
<head>
<title>blah</title>
</head>
<body>
<p> blah blah example@example.com</p>
<a href="example.com">link</a>
</body>
</html>
'''


class TestDefaultHTMLHandler(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()
