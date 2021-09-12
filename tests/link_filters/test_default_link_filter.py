from extract_emails.link_filters import DefaultLinkFilter


def test_default_link_filter():
    test_urls = ["https://example.com", "/page.html", "https://google.com"]
    filtered_urls = DefaultLinkFilter.filter(test_urls)

    assert "https://google.com" not in filtered_urls
    assert len(filtered_urls) == 2
