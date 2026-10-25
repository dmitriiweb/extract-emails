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


def test_get_data_preserves_mixed_case_email():
    email = "User@Example.COM"

    assert EmailExtractor().get_data(email) == {email}


def test_get_data_keeps_adjacent_quoted_email_boundaries():
    page_source = r'"alice"@Example.COM,"bob"@example.com'

    assert EmailExtractor().get_data(page_source) == {
        '"alice"@Example.COM',
        '"bob"@example.com',
    }


def test_get_data_accepts_escaped_quote_in_quoted_local_part():
    email = r'"al\"ice"@Example.COM'

    assert EmailExtractor().get_data(email) == {email}
