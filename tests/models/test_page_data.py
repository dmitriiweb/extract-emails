import asyncio
import csv
import inspect
from collections.abc import Callable
from pathlib import Path

import pytest

from extract_emails.models import PageData

CSVMethod = Callable[[list[PageData], Path], None]


def page(data=None, page_url="https://example.com/page"):
    return PageData(website="https://example.com", page_url=page_url, data=data or {})


def save(method: CSVMethod, pages: list[PageData], path: Path) -> None:
    result = method(pages, path)
    if inspect.isawaitable(result):
        asyncio.run(result)


def read_csv(path: Path):
    with path.open(encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        return reader.fieldnames, list(reader)


@pytest.mark.parametrize("method", [PageData.to_csv, PageData.ato_csv])
def test_page_data_csv_preserves_values_with_reordered_and_missing_labels(
    tmp_path, method
):
    path = tmp_path / "contacts.csv"
    pages = [
        page({"email": ["one@example.com", "two@example.com"], "profile": ["p1"]}),
        page(
            {
                "profile": ["p2", "p3"],
                "email": ["three@example.com"],
                "company": ["c1"],
            },
            "https://example.com/second",
        ),
        page({"company": ["c2", "c3"]}, "https://example.com/third"),
    ]

    save(method, pages, path)

    headers, rows = read_csv(path)
    assert headers == ["website", "page_url", "email", "profile", "company"]
    assert [(row["email"], row["profile"], row["company"]) for row in rows] == [
        ("one@example.com", "p1", ""),
        ("two@example.com", "", ""),
        ("three@example.com", "p2", "c1"),
        ("", "p3", ""),
        ("", "", "c2"),
        ("", "", "c3"),
    ]


@pytest.mark.parametrize("method", [PageData.to_csv, PageData.ato_csv])
def test_page_data_csv_empty_input_does_not_create_or_change_file(tmp_path, method):
    path = tmp_path / "contacts.csv"
    save(method, [], path)
    assert not path.exists()

    path.write_bytes(b"existing contents\n")
    before = path.read_bytes()
    save(method, [], path)
    assert path.read_bytes() == before


@pytest.mark.parametrize("method", [PageData.to_csv, PageData.ato_csv])
def test_page_data_csv_writes_header_to_existing_empty_file(tmp_path, method):
    path = tmp_path / "contacts.csv"
    path.touch()

    save(method, [page({"email": ["one@example.com"]})], path)

    headers, rows = read_csv(path)
    assert headers == ["website", "page_url", "email"]
    assert rows[0]["email"] == "one@example.com"


@pytest.mark.parametrize("method", [PageData.to_csv, PageData.ato_csv])
def test_page_data_csv_matching_append_keeps_existing_rows(tmp_path, method):
    path = tmp_path / "contacts.csv"
    save(method, [page({"email": ["one@example.com"]})], path)

    save(
        method,
        [page({"email": ["two@example.com"]}, "https://example.com/next")],
        path,
    )

    assert [row["email"] for row in read_csv(path)[1]] == [
        "one@example.com",
        "two@example.com",
    ]


@pytest.mark.parametrize("method", [PageData.to_csv, PageData.ato_csv])
def test_page_data_csv_rejects_mismatched_append_without_changes(tmp_path, method):
    path = tmp_path / "contacts.csv"
    save(method, [page({"email": ["one@example.com"]})], path)
    before = path.read_bytes()

    with pytest.raises(ValueError, match="CSV header mismatch"):
        save(method, [page({"profile": ["profile"]})], path)

    assert path.read_bytes() == before


@pytest.mark.parametrize("method", [PageData.to_csv, PageData.ato_csv])
def test_page_data_csv_zero_labels_writes_metadata_header_without_rows(
    tmp_path, method
):
    path = tmp_path / "contacts.csv"

    save(method, [page()], path)

    headers, rows = read_csv(path)
    assert headers == ["website", "page_url"]
    assert rows == []


@pytest.mark.parametrize("method", [PageData.to_csv, PageData.ato_csv])
def test_page_data_csv_all_empty_labels_writes_header_without_rows(tmp_path, method):
    path = tmp_path / "contacts.csv"

    save(method, [page({"email": [], "profile": []})], path)

    headers, rows = read_csv(path)
    assert headers == ["website", "page_url", "email", "profile"]
    assert rows == []


@pytest.mark.parametrize("method", [PageData.to_csv, PageData.ato_csv])
def test_page_data_csv_renames_metadata_aliases_without_changing_page_data(
    tmp_path, method
):
    path = tmp_path / "contacts.csv"
    first = page(
        {
            "website": ["website payload"],
            "page_url": ["url payload"],
            "data.website": ["literal website"],
            "email": ["a@example.com"],
        }
    )
    second = page(
        {
            "website": [],
            "page_url": ["second url"],
            "data.data.website": ["literal nested", "second nested"],
        },
        "https://example.com/second",
    )
    original = [
        {key: values.copy() for key, values in item.data.items()}
        for item in (first, second)
    ]

    save(method, [first, second], path)

    headers, rows = read_csv(path)
    assert headers == [
        "website",
        "page_url",
        "data.website",
        "data.page_url",
        "data.data.website",
        "email",
        "data.data.data.website",
    ]
    assert rows == [
        {
            "website": "https://example.com",
            "page_url": "https://example.com/page",
            "data.website": "website payload",
            "data.page_url": "url payload",
            "data.data.website": "literal website",
            "email": "a@example.com",
            "data.data.data.website": "",
        },
        {
            "website": "https://example.com",
            "page_url": "https://example.com/second",
            "data.website": "",
            "data.page_url": "second url",
            "data.data.website": "",
            "email": "",
            "data.data.data.website": "literal nested",
        },
        {
            "website": "https://example.com",
            "page_url": "https://example.com/second",
            "data.website": "",
            "data.page_url": "",
            "data.data.website": "",
            "email": "",
            "data.data.data.website": "second nested",
        },
    ]
    assert [first.data, second.data] == original


@pytest.mark.parametrize("method", [PageData.to_csv, PageData.ato_csv])
def test_page_data_csv_append_uses_stable_escaped_columns(tmp_path, method):
    path = tmp_path / "contacts.csv"
    save(method, [page({"website": ["first"]})], path)
    save(method, [page({"website": ["second"]})], path)

    headers, rows = read_csv(path)
    assert headers == ["website", "page_url", "data.website"]
    assert [row["data.website"] for row in rows] == ["first", "second"]

    before = path.read_bytes()
    with pytest.raises(ValueError, match="CSV header mismatch"):
        save(method, [page({"data.website": ["literal"]})], path)
    assert path.read_bytes() == before
