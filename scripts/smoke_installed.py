#!/usr/bin/env python3
"""Exercise imports and the installed CLI from an isolated wheel environment."""

from __future__ import annotations

import argparse
import csv
import importlib.util
import os
import subprocess
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from tempfile import TemporaryDirectory
from threading import Thread

EXTRAS = ("base", "httpx", "playwright", "all")


class _FixtureHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        body = (
            b"<!doctype html><html><body>contact@example.com "
            b"https://www.linkedin.com/in/fixture-person</body></html>"
        )
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:
        pass


def _expect_missing_backend(name: str, extra: str) -> None:
    try:
        getattr(__import__("extract_emails.browsers", fromlist=[name]), name)
    except ImportError as error:
        if f"extract-emails[{extra}]" not in str(error):
            raise AssertionError(
                f"Missing {name} error did not name its extra"
            ) from error
    else:
        raise AssertionError(f"{name} imported without its {extra} dependency")


def _assert_imports(extra: str) -> None:
    import extract_emails
    import extract_emails.data_extractors
    import extract_emails.models
    from extract_emails.data_extractors.advanced_email_extractor import (
        AdvancedEmailExtractor,
    )

    advanced = AdvancedEmailExtractor()
    assert advanced.get_data("<p>advanced@example.com</p>") == {"advanced@example.com"}
    if importlib.util.find_spec("cssselect") is not None:
        raise AssertionError("Smoke environment unexpectedly includes cssselect")
    assert (
        Path(extract_emails.__file__)
        .resolve()
        .is_relative_to(Path(sys.prefix).resolve())
    ), "Imports must resolve to the installed wheel, not the checkout"
    source = "User@Example.COM https://LinkedIn.com/in/fixture"
    page = extract_emails.models.PageData(
        website="https://example.com",
        page_url="https://example.com",
        data={
            "email": list(
                extract_emails.data_extractors.EmailExtractor().get_data(source)
            ),
            "linkedin": list(
                extract_emails.data_extractors.LinkedinExtractor().get_data(source)
            ),
        },
    )
    assert page.data == {
        "email": ["User@Example.COM"],
        "linkedin": ["https://LinkedIn.com/in/fixture"],
    }

    has_httpx = extra in ("httpx", "all")
    has_playwright = extra in ("playwright", "all")
    assert (importlib.util.find_spec("httpx") is not None) == has_httpx
    assert (importlib.util.find_spec("playwright") is not None) == has_playwright

    from extract_emails import browsers

    if has_httpx:
        browsers.HttpxBrowser().stop()
    else:
        _expect_missing_backend("HttpxBrowser", "httpx")
    if has_playwright:
        browsers.ChromiumBrowser().stop()
    else:
        _expect_missing_backend("ChromiumBrowser", "playwright")


def _installed_cli() -> Path:
    executable = Path(sys.executable).with_name("extract-emails")
    if os.name == "nt":
        executable = executable.with_suffix(".exe")
    if not executable.exists():
        raise AssertionError(f"Installed CLI not found: {executable}")
    return executable


def _run_cli_help() -> None:
    subprocess.run([str(_installed_cli()), "--help"], check=True, cwd=Path.cwd())


def _run_cli_smoke() -> None:
    executable = _installed_cli()
    server = ThreadingHTTPServer(("127.0.0.1", 0), _FixtureHandler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        with TemporaryDirectory(prefix="extract-emails-cli-") as directory:
            output = Path(directory) / "results.csv"
            subprocess.run(
                [
                    str(executable),
                    "--url",
                    f"http://127.0.0.1:{server.server_port}/",
                    "--output-file",
                    str(output),
                    "--browser-name",
                    "httpx",
                    "--data-type",
                    "email,linkedin",
                ],
                check=True,
                cwd=directory,
            )
            with output.open(encoding="utf-8", newline="") as csv_file:
                rows = list(csv.DictReader(csv_file))
            if not rows:
                raise AssertionError("Installed CLI produced no CSV rows")
            emails = {row.get("email", "") for row in rows}
            linkedin = {row.get("linkedin", "") for row in rows}
            if "contact@example.com" not in emails:
                raise AssertionError(
                    f"Email column did not contain fixture email: {emails}"
                )
            if "https://www.linkedin.com/in/fixture-person" not in linkedin:
                raise AssertionError(
                    f"LinkedIn column did not contain fixture URL: {linkedin}"
                )
    finally:
        server.shutdown()
        server.server_close()
        thread.join()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--extra", choices=EXTRAS, required=True)
    args = parser.parse_args()

    _assert_imports(args.extra)
    _run_cli_help()
    if args.extra in ("httpx", "all"):
        _run_cli_smoke()
    print(f"Installed wheel smoke passed for extra={args.extra}")


if __name__ == "__main__":
    main()
