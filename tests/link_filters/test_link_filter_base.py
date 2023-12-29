from extract_emails.link_filters import LinkFilterBase

HTML_EXAMPLE = """
<!doctype html>
<head>
<title>blah</title>
</head>
<body>
<a href="example.com">link</a>
<a href="/example2.com">link</a>
<a href="https://example2.com">link</a>
</body>
</html>
"""


def test_get_website_address_valid_url():
    website = LinkFilterBase.get_website_address("https://example.com/list?page=1")
    assert website == "https://example.com/"

    website = LinkFilterBase.get_website_address(
        "https://subexample.example.com/list?page=1"
    )
    assert website == "https://subexample.example.com/"


def test_get_links():
    links = LinkFilterBase.get_links(HTML_EXAMPLE)
    assert links == ["example.com", "/example2.com", "https://example2.com"]
