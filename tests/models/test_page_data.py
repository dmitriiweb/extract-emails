import pytest

from extract_emails.models import PageData


@pytest.fixture
def page_data():
    return PageData(
        website="https://example.com", page_url="https://example.com/page=123"
    )


def test_model_init(page_data: PageData):
    assert isinstance(page_data.data, dict)


def test_add_vals(page_data: PageData):
    page_data.append("emails", ["email@email.com"])
    assert "emails" in page_data.data
    assert "email@email.com" == page_data.data["emails"][0]


def test_len(page_data: PageData):
    page_data.append("emails", ["email@email.com", "email@email.com2"])
    page_data.append("emails2", ["email@email.com", "email@email.com2"])

    assert len(page_data) == 4
