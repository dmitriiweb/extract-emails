import csv
from pathlib import Path

import pytest
from click.testing import CliRunner

from extract_emails.browsers.page_source_getter import PageSourceGetter
from extract_emails.console import application


class LocalBrowser(PageSourceGetter):
    def __init__(self, page_source: str = "") -> None:
        self.page_source = page_source
        self.started = False
        self.stopped = False

    def start(self) -> None:
        self.started = True

    def stop(self) -> None:
        self.stopped = True

    async def astart(self) -> None:
        self.start()

    async def astop(self) -> None:
        self.stop()

    def get_page_source(self, url: str) -> str:
        return self.page_source

    async def aget_page_source(self, url: str) -> str:
        return self.page_source


def test_cli_extracts_requested_data_in_first_occurrence_order(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    browser = LocalBrowser(
        "Contact user@example.com at https://www.linkedin.com/in/example-person"
    )
    monkeypatch.setattr(application, "get_browser", lambda name: browser)
    output = tmp_path / "contacts.csv"

    result = CliRunner().invoke(
        application.main,
        [
            "--url",
            "https://example.com/",
            "--output-file",
            str(output),
            "--browser-name",
            "httpx",
            "--data-type",
            " linkedin, email,linkedin ",
        ],
    )

    assert result.exit_code == 0, result.output
    with output.open(encoding="utf-8", newline="") as csv_file:
        rows = list(csv.DictReader(csv_file))
    assert list(rows[0]) == ["website", "page_url", "linkedin", "email"]
    assert rows[0]["email"] == "user@example.com"
    assert rows[0]["linkedin"] == "https://www.linkedin.com/in/example-person"
    assert browser.started and browser.stopped


def test_cli_defaults_to_email_extraction(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    browser = LocalBrowser("Contact user@example.com")
    selected_browsers: list[str] = []

    def get_browser(name: str) -> PageSourceGetter:
        selected_browsers.append(name)
        return browser

    monkeypatch.setattr(application, "get_browser", get_browser)
    output = tmp_path / "contacts.csv"

    result = CliRunner().invoke(
        application.main,
        ["--url", "https://example.com/", "--output-file", str(output)],
    )

    assert result.exit_code == 0, result.output
    with output.open(encoding="utf-8", newline="") as csv_file:
        rows = list(csv.DictReader(csv_file))
    assert list(rows[0]) == ["website", "page_url", "email"]
    assert rows[0]["email"] == "user@example.com"
    assert selected_browsers == ["chromium"]


@pytest.mark.parametrize("data_type", ["email,,linkedin", "email,unknown", ",email"])
def test_cli_rejects_invalid_data_type_before_browser_creation(
    data_type: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    def unexpected_browser(name: str) -> PageSourceGetter:
        pytest.fail("Browser must not be resolved for invalid data types")

    monkeypatch.setattr(application, "get_browser", unexpected_browser)
    result = CliRunner().invoke(
        application.main,
        [
            "--url",
            "https://example.com",
            "--output-file",
            "out.csv",
            "--data-type",
            data_type,
        ],
    )

    assert result.exit_code == 2


def test_cli_rejects_invalid_browser_before_browser_creation(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def unexpected_browser(name: str) -> PageSourceGetter:
        pytest.fail("Browser must not be resolved for an invalid browser choice")

    monkeypatch.setattr(application, "get_browser", unexpected_browser)
    result = CliRunner().invoke(
        application.main,
        [
            "--url",
            "https://example.com",
            "--output-file",
            "out.csv",
            "--browser-name",
            "firefox",
        ],
    )

    assert result.exit_code == 2


def test_cli_closes_browser_when_worker_fails(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    browser = LocalBrowser()
    monkeypatch.setattr(application, "get_browser", lambda name: browser)

    class FailingWorker:
        def __init__(self, **kwargs: object) -> None:
            pass

        def get_data(self) -> list[object]:
            raise RuntimeError("worker failed")

    monkeypatch.setattr(application, "DefaultWorker", FailingWorker)
    output = tmp_path / "contacts.csv"

    result = CliRunner().invoke(
        application.main,
        ["--url", "https://example.com", "--output-file", str(output)],
    )

    assert result.exit_code == 1
    assert isinstance(result.exception, RuntimeError)
    assert browser.started and browser.stopped
    assert not output.exists()
