from extract_emails.utils import email_filter


def test_email_filter():
    test_emails = ["email@email.com", "email@email.com", "2@pic.png"]
    filtered_emails = email_filter(test_emails)

    assert len(filtered_emails) == 1
    assert "email@email.com" in filtered_emails


def test_email_filter_compares_tld_case_insensitively_and_preserves_input():
    email = "User@Example.COM"

    assert email_filter([email]) == {email}


def test_email_filter_accepts_unicode_tld_from_snapshot():
    email = "user@example.рф"

    assert email_filter([email]) == {email}


def test_email_filter_does_not_infer_unlisted_punycode_tld():
    assert email_filter(["user@example.xn--p1ai"]) == set()


def test_email_filter_preserves_reserved_domain_acceptance():
    assert email_filter(["user@example.arpa"]) == {"user@example.arpa"}


def test_email_filter_uses_normalized_snapshot_entries():
    emails = [
        "user@example.бг",
        "user@example.ελ",
        "user@example.institute",
        "user@example.الجزائر",
    ]

    assert email_filter(emails) == set(emails)
