import pytest

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


def test_get_links_supports_uppercase_and_unquoted_attributes():
    page_source = "<A HREF=https://example.com/profile>Profile</A>"

    assert LinkFilterBase.get_links(page_source) == ["https://example.com/profile"]


def test_get_links_returns_empty_for_empty_or_invalid_html():
    assert LinkFilterBase.get_links("") == []
    assert LinkFilterBase.get_links("\x00") == []


@pytest.mark.parametrize("quote", ['"', "'"])
@pytest.mark.parametrize("encoding", ["UTF-8", "ISO-8859-1"])
def test_get_links_parses_decoded_unicode_after_xml_declaration(quote, encoding):
    page_source = (
        f"<?xml version={quote}1.0{quote} encoding={quote}{encoding}{quote}?>"
        '<a href="/联系/é">contact</a>'
    )

    assert LinkFilterBase.get_links(page_source) == ["/联系/é"]


def test_get_links_preserves_leading_space_and_bom_before_xml_declaration():
    page_source = '\ufeff \n<?xml version="1.0"?><a href="/contact">contact</a>'

    assert LinkFilterBase.get_links(page_source) == ["/contact"]


def test_get_links_does_not_strip_xml_stylesheet_instruction():
    page_source = (
        '<?xml-stylesheet type="text/xsl" href="style.xsl"?>'
        '<a href="/contact">contact</a>'
    )

    assert LinkFilterBase.get_links(page_source) == ["/contact"]
