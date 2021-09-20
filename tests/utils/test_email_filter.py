from extract_emails.utils import email_filter


def test_email_filter():
    test_emails = ["email@email.com", "email@email.com", "2@pic.png"]
    filtered_emails = email_filter(test_emails)

    assert len(filtered_emails) == 1
    assert "email@email.com" in filtered_emails
