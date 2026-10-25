import csv

import pytest

from extract_emails.data_savers.csv_saver import CsvSaver
from extract_emails.models import PageData


def page(data=None, page_url="https://example.com/page"):
    return PageData(website="https://example.com", page_url=page_url, data=data or {})


def make_saver(path, mode="w"):
    return CsvSaver(save_mode=mode, output_path=path)


def read_csv(path):
    with path.open(encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        return reader.fieldnames, list(reader)


@pytest.mark.parametrize("mode", ["w", "wt", "tw", "w+", "tw+"])
def test_csv_saver_write_modes_overwrite_with_header_and_all_values(tmp_path, mode):
    path = tmp_path / "contacts.csv"
    path.write_text("stale content\n", encoding="utf-8")
    pages = [
        page({"email": ["one@example.com", "two@example.com"], "profile": ["p1"]}),
        page({"profile": ["p2", "p3"], "other": ["o1"]}),
    ]

    make_saver(path, mode).save(pages)

    headers, rows = read_csv(path)
    assert headers == ["website", "page", "email", "profile", "other"]
    assert [row["email"] for row in rows] == [
        "one@example.com",
        "two@example.com",
        "",
        "",
    ]
    assert [row["profile"] for row in rows] == ["p1", "", "p2", "p3"]
    assert [row["other"] for row in rows] == ["", "", "o1", ""]


@pytest.mark.parametrize("mode", ["a", "at", "ta", "a+", "ta+"])
@pytest.mark.parametrize("initial_state", ["missing", "empty"])
def test_csv_saver_append_modes_write_header_for_missing_or_empty_files(
    tmp_path, mode, initial_state
):
    path = tmp_path / "contacts.csv"
    if initial_state == "empty":
        path.touch()

    make_saver(path, mode).save([page({"email": ["one@example.com"]})])

    headers, rows = read_csv(path)
    assert headers == ["website", "page", "email"]
    assert [row["email"] for row in rows] == ["one@example.com"]


@pytest.mark.parametrize("mode", ["a", "at", "ta", "a+", "ta+"])
def test_csv_saver_append_modes_accept_matching_header_without_duplicates(
    tmp_path, mode
):
    path = tmp_path / "contacts.csv"
    saver = make_saver(path, mode)
    saver.save([page({"email": ["one@example.com"]})])
    saver.save([page({"email": ["two@example.com"]}, "https://example.com/next")])

    headers, rows = read_csv(path)
    assert headers == ["website", "page", "email"]
    assert [row["email"] for row in rows] == ["one@example.com", "two@example.com"]


@pytest.mark.parametrize(
    ("mode", "incoming_label"),
    [
        ("a", "profile"),
        ("at", "profile"),
        ("ta", "linkedin"),
        ("a+", "profile"),
        ("ta+", "profile"),
    ],
)
def test_csv_saver_append_modes_reject_mismatches_without_changes(
    tmp_path, mode, incoming_label
):
    path = tmp_path / "contacts.csv"
    saver = make_saver(path, mode)
    saver.save([page({"email": ["one@example.com"]})])
    before = path.read_bytes()

    with pytest.raises(ValueError, match="CSV header mismatch"):
        saver.save([page({incoming_label: ["incoming"]})])

    assert path.read_bytes() == before


@pytest.mark.parametrize("mode", ["x", "xt", "tx"])
def test_csv_saver_exclusive_modes_write_header_and_preserve_existing_file(
    tmp_path, mode
):
    path = tmp_path / "contacts.csv"
    make_saver(path, mode).save(
        [page({"email": ["one@example.com", "two@example.com"]})]
    )
    headers, rows = read_csv(path)
    assert headers == ["website", "page", "email"]
    assert [row["email"] for row in rows] == ["one@example.com", "two@example.com"]

    before = path.read_bytes()
    with pytest.raises(FileExistsError):
        make_saver(path, mode).save([page({"email": ["three@example.com"]})])
    assert path.read_bytes() == before


@pytest.mark.parametrize(
    "mode",
    ["w", "wt", "tw", "w+", "tw+", "a", "at", "ta", "a+", "ta+", "x", "xt", "tx"],
)
def test_csv_saver_empty_input_does_not_create_or_truncate(tmp_path, mode):
    path = tmp_path / "contacts.csv"
    make_saver(path, mode).save([])
    assert not path.exists()
    path.write_bytes(b"existing")
    make_saver(path, mode).save([])
    assert path.read_bytes() == b"existing"


def test_csv_saver_process_data_keeps_multiple_values_and_first_seen_labels():
    rows = CsvSaver.process_data(
        [
            page({"email": ["one@example.com", "two@example.com"], "profile": ["p1"]}),
            page({"profile": ["p2"], "other": ["o1"]}),
        ]
    )
    assert [row["email"] for row in rows] == ["one@example.com", "two@example.com", ""]
    assert [row["profile"] for row in rows] == ["p1", "", "p2"]
    assert [row["other"] for row in rows] == ["", "", "o1"]


def test_csv_saver_zero_and_all_empty_labels_write_headers_without_rows(tmp_path):
    path = tmp_path / "contacts.csv"
    make_saver(path).save([page(), page({"email": [], "profile": []})])

    headers, rows = read_csv(path)
    assert headers == ["website", "page", "email", "profile"]
    assert rows == []


def test_csv_saver_renames_metadata_aliases_in_files_and_processed_rows(tmp_path):
    data = {
        "website": ["website payload"],
        "page": ["page payload"],
        "page_url": ["url payload"],
        "email": ["a@example.com"],
    }
    item = page(data, "https://example.com/source")

    rows = CsvSaver.process_data([item])
    assert rows == [
        {
            "website": "https://example.com",
            "page": "https://example.com/source",
            "data.website": "website payload",
            "data.page": "page payload",
            "page_url": "url payload",
            "email": "a@example.com",
        }
    ]
    assert CsvSaver.get_headers(rows) == [
        "website",
        "page",
        "data.website",
        "data.page",
        "page_url",
        "email",
    ]

    path = tmp_path / "contacts.csv"
    make_saver(path).save([item])
    headers, saved_rows = read_csv(path)
    assert headers == CsvSaver.get_headers(rows)
    assert saved_rows == rows
    assert item.data == data


def test_csv_saver_append_uses_stable_escaped_columns(tmp_path):
    path = tmp_path / "contacts.csv"
    saver = make_saver(path, "a")
    saver.save([page({"website": ["first"]})])
    saver.save([page({"website": ["second"]})])

    headers, rows = read_csv(path)
    assert headers == ["website", "page", "data.website"]
    assert [row["data.website"] for row in rows] == ["first", "second"]

    before = path.read_bytes()
    with pytest.raises(ValueError, match="CSV header mismatch"):
        saver.save([page({"data.website": ["literal"]})])
    assert path.read_bytes() == before
