from extract_emails.data_extractors.advanced_email_extractor import (
    AdvancedEmailExtractor,
)


def _encode_cloudflare_email(email: str, key: int = 0x2A) -> str:
    return f"{key:02x}" + "".join(f"{ord(char) ^ key:02x}" for char in email)


def test_get_data_extracts_plain_and_cloudflare_emails():
    encoded = _encode_cloudflare_email("Protected@Example.com")
    page = f'<p>plain@example.com</p><span data-cfemail="{encoded}"></span>'

    assert AdvancedEmailExtractor().get_data(page) == {
        "plain@example.com",
        "protected@example.com",
    }


def test_get_data_skips_malformed_cloudflare_attributes():
    valid = _encode_cloudflare_email("valid@example.com")
    invalid_values = ("zz", "2a1", "", "2a")
    attributes = "".join(
        f'<span data-cfemail="{value}"></span>' for value in invalid_values
    )
    page = f'<span data-cfemail="{valid}"></span>{attributes}'

    assert AdvancedEmailExtractor().get_data(page) == {"valid@example.com"}


def test_get_data_rejects_decoded_non_email_cloudflare_values():
    encoded = _encode_cloudflare_email("not-an-email")
    page = f'<span data-cfemail="{encoded}"></span>'

    assert AdvancedEmailExtractor().get_data(page) == set()


def test_get_data_keeps_plain_emails_when_html_parser_fails(monkeypatch):
    def raise_parser_error(_page_source):
        raise ValueError("invalid HTML")

    monkeypatch.setattr(
        "extract_emails.data_extractors.advanced_email_extractor.html.fromstring",
        raise_parser_error,
    )

    assert AdvancedEmailExtractor().get_data("plain@example.com") == {
        "plain@example.com"
    }


def test_get_data_accepts_empty_html():
    assert AdvancedEmailExtractor().get_data("") == set()
