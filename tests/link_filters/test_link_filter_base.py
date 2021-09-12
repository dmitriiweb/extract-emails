from extract_emails.link_filters import LinkFilterBase


def test_get_website_address_valid_url():
    website = LinkFilterBase.get_website_address("https://example.com/list?page=1")
    assert website == "https://example.com/"

    website = LinkFilterBase.get_website_address(
        "https://subexample.example.com/list?page=1"
    )
    assert website == "https://subexample.example.com/"
