import pytest

from extract_emails.models import PageData


@pytest.fixture
def page_data():
    return PageData(
        website="https://example.com", page_url="https://example.com/page=123"
    )


def test_model_init(page_data: PageData):
    assert isinstance(page_data.data, dict)
