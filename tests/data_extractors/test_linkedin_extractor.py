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
