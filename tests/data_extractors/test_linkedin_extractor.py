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
