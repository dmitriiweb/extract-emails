import pytest

from extract_emails.link_filters import ContactInfoLinkFilter

test_urls = [
    "https://google.com",
    "/page1",
    "https://example.com/page",
    "https://example.com/about",
    "/about-us",
    "/about-us",
    "https://example.com/not-default-call-us",
    "https://example.com/not-default-call-us-2",
    "/not-default-call-us-2",
]


def test_default_candidates():
    link_filter = ContactInfoLinkFilter("https://example.com")
    filtered_links = link_filter.filter(test_urls)
    assert len(filtered_links) == 2
    assert "https://google.com" not in filtered_links
    assert "https://example.com/page1" not in filtered_links


def test_custom_candidates():
    link_filter = ContactInfoLinkFilter("https://example.com", ["call-us"])
    filtered_links = link_filter.filter(test_urls)
    assert len(filtered_links) == 2
    assert "https://google.com" not in filtered_links
    assert "https://example.com/page1" not in filtered_links
    assert "https://example.com/not-default-call-us-2" in filtered_links


def test_use_default_true():
    link_filter = ContactInfoLinkFilter(
        "https://example.com", ["not-call-us"], use_default=True
    )
    filtered_links = link_filter.filter(test_urls)
    assert len(filtered_links) == 6
    assert "https://example.com/page" in filtered_links


def test_use_default_false():
    link_filter = ContactInfoLinkFilter(
        "https://example.com", ["not-call-us"], use_default=False
    )
    filtered_links = link_filter.filter(test_urls)
    assert len(filtered_links) == 0
