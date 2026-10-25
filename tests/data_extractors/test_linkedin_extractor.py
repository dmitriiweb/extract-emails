import pytest

from extract_emails.data_extractors import LinkedinExtractor

STRING = """
The good thing about your LinkedIn URL is that you can have your customized URL. By default, LinkedIn will provide you a profile URL that is alphanumeric and is a combination of your name and numbers.
For example, it will look something similar to this: https://www.linkedin.com/in/venjamin-brant-73381ujy3u
The good thing about your LinkedIn URL is that you can have your customized URL. By default, LinkedIn will provide you a profile URL that is alphanumeric and is a combination of your name and numbers.
For example, it will look something similar to this: https://www.linkedin.com/in/venjamin-brant-73381ujy3u
"""


def test_linkedin_get_data():
    linkedin_extractor = LinkedinExtractor()
    urls = linkedin_extractor.get_data(STRING)
    assert len(urls) == 1
    assert "https://www.linkedin.com/in/venjamin-brant-73381ujy3u" in urls


def test_linkedin_get_data_accepts_case_insensitive_linkedin_hosts():
    page_source = """
    https://LinkedIn.com/in/alice
    www.linkedin.com/in/bob
    https://careers.linkedin.com/in/carol
    """

    assert LinkedinExtractor().get_data(page_source) == {
        "https://LinkedIn.com/in/alice",
        "www.linkedin.com/in/bob",
        "https://careers.linkedin.com/in/carol",
    }


def test_linkedin_get_data_rejects_impostor_hosts_and_paths():
    page_source = """
    https://linkedin.com.evil.example/in/attacker
    https://evil-linkedin.com/in/attacker
    https://evil.example/linkedin.com/in/attacker
    """

    assert LinkedinExtractor().get_data(page_source) == set()


def test_linkedin_get_data_skips_malformed_candidates():
    page_source = "https://[invalid/path https://LinkedIn.com/in/valid"

    assert LinkedinExtractor().get_data(page_source) == {
        "https://LinkedIn.com/in/valid"
    }


def test_linkedin_get_data_stops_at_html_attribute_delimiters():
    page_source = (
        '<a href="https://www.linkedin.com/in/alice" '
        'class="profile">LinkedIn profile</a>'
    )

    assert LinkedinExtractor().get_data(page_source) == {
        "https://www.linkedin.com/in/alice"
    }


@pytest.mark.parametrize(
    "suffix",
    [
        r"\&quot;&gt;LinkedIn&lt;\/a&gt;&lt;\/p&gt;",
        "&quot;",
        "&apos;",
        "&#34;",
        "&#x22;",
        "&lt;/a&gt;",
    ],
)
def test_linkedin_get_data_stops_at_serialized_html_delimiters(suffix):
    url = "https://www.linkedin.com/in/alice"

    assert LinkedinExtractor().get_data(url + suffix) == {url}


def test_linkedin_get_data_stops_at_json_escaped_quote_delimiters():
    url = "https://www.linkedin.com/in/alice"

    assert LinkedinExtractor().get_data(url + r"\",\"target\":\"_blank\"") == {url}


def test_linkedin_get_data_extracts_adjacent_json_urls():
    page_source = (
        r"[\"https://www.linkedin.com/in/alice/\","
        r"\"https://www.linkedin.com/in/bob/\"]"
    )

    assert LinkedinExtractor().get_data(page_source) == {
        "https://www.linkedin.com/in/alice/",
        "https://www.linkedin.com/in/bob/",
    }


def test_linkedin_get_data_deduplicates_clean_and_escaped_urls():
    url = "https://www.linkedin.com/in/alice"

    assert LinkedinExtractor().get_data(
        url + " " + url + r"\",\"target\":\"_blank\""
    ) == {url}


def test_linkedin_get_data_keeps_valid_links_after_malformed_candidate():
    valid_url = "https://LinkedIn.com/in/Alice"
    page_source = (
        "https://www.linkedin.com/in/broken" + r"\&quot;&gt;not-a-profile " + valid_url
    )

    assert LinkedinExtractor().get_data(page_source) == {
        "https://www.linkedin.com/in/broken",
        valid_url,
    }


def test_linkedin_get_data_preserves_valid_profile_url_forms():
    page_source = """
    linkedin.com/in/Alice%20Smith
    https://www.linkedin.com/in/José-李
    https://www.linkedin.com/in/Alice?view=full&not=1&copy=2#Contact
    https://www.linkedin.com/in/Alice?filter=(recent)
    """

    assert LinkedinExtractor().get_data(page_source) == {
        "linkedin.com/in/Alice%20Smith",
        "https://www.linkedin.com/in/José-李",
        "https://www.linkedin.com/in/Alice?view=full&not=1&copy=2#Contact",
        "https://www.linkedin.com/in/Alice?filter=(recent)",
    }


def test_linkedin_get_data_decodes_html_ampersands_in_query_strings():
    raw_url = "https://www.linkedin.com/in/Alice?view=full&not=1&copy=2#Contact"
    encoded_url = (
        "https://www.linkedin.com/in/Alice?view=full&amp;not=1&amp;copy=2#Contact"
    )

    assert LinkedinExtractor().get_data(raw_url + " " + encoded_url) == {raw_url}
