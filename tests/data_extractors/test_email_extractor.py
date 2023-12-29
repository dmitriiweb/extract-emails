from extract_emails.data_extractors import EmailExtractor

STRING = """
blah blah email@example.com blah blah
blah blah "email2@example.com" blah blah
blah blah "email2@example.com" blah blah
"""


def test_get_data():
    email_extractor = EmailExtractor()
    emails = email_extractor.get_data(STRING)

    assert "email2@example.com" in emails
    assert len(emails) == 2
