from extract_emails.link_filters import DefaultLinkFilter


def test_default_link_filter():
    test_urls = [
        "https://example.com/page1.html",
        "/page.html",
        "/page.html",
        "https://google.com",
    ]
    link_filter = DefaultLinkFilter("https://example.com/")
    filtered_urls = link_filter.filter(test_urls)

    assert "https://google.com" not in filtered_urls
    assert len(filtered_urls) == 2
