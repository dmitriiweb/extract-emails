#!/usr/bin/env python3
"""Run with: uv run python scripts/one_time_live_extraction.py [--targets PATH] [--output PATH]."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any

from extract_emails.browsers import HttpxBrowser
from extract_emails.data_extractors import EmailExtractor, LinkedinExtractor
from extract_emails.models import PageData
from extract_emails.workers import DefaultWorker

DEFAULT_TARGETS = Path(__file__).resolve().with_name("live_targets.json")
DEFAULT_OUTPUT = Path("live_extraction_results.json")
SITE_DELAY_SECONDS = 1.0


class _RecordingHttpxBrowser(HttpxBrowser):
    """Record empty responses and raised fetch errors without using private clients."""

    def __init__(self) -> None:
        super().__init__()
        self.page_status: dict[str, str] = {}

    def get_page_source(self, url: str) -> str:
        try:
            source = super().get_page_source(url)
        except Exception as error:
            self.page_status[url] = f"error: {type(error).__name__}: {error}"
            raise
        if not source:
            self.page_status[url] = "empty_response"
        else:
            self.page_status[url] = "fetched"
        return source


def _positive_int(value: str) -> int:
    try:
        number = int(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("must be an integer of at least 1") from error
    if number < 1:
        raise argparse.ArgumentTypeError(
            "must be at least 1 (zero would mean unlimited)"
        )
    return number


def _nonnegative_int(value: str) -> int:
    try:
        number = int(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("must be a non-negative integer") from error
    if number < 0:
        raise argparse.ArgumentTypeError("must be non-negative")
    return number


def _load_targets(path: Path) -> list[dict[str, str]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError("targets manifest must be a JSON array")
    targets: list[dict[str, str]] = []
    for index, item in enumerate(payload):
        if not isinstance(item, dict) or not all(
            isinstance(item.get(key), str) and item[key].strip()
            for key in ("name", "url", "reason")
        ):
            raise ValueError(
                f"target {index} must have non-empty name, url, and reason strings"
            )
        targets.append({key: item[key] for key in ("name", "url", "reason")})
    return targets


def _page_result(page: PageData, status: str) -> dict[str, Any]:
    return {
        "source_url": page.page_url,
        "status": status,
        "emails": sorted(set(page.data.get("email", []))),
        "linkedin": sorted(set(page.data.get("linkedin", []))),
    }


def _extract_site(
    target: dict[str, str], browser: _RecordingHttpxBrowser, depth: int, max_links: int
) -> dict[str, Any]:
    browser.page_status.clear()
    errors: list[dict[str, str]] = []
    pages: list[dict[str, Any]] = []
    try:
        worker = DefaultWorker(
            target["url"],
            browser,
            data_extractors=[EmailExtractor(), LinkedinExtractor()],
            depth=depth,
            max_links_from_page=max_links,
        )
        extracted = worker.get_data()
        for page in extracted:
            fetch_status = browser.page_status.get(page.page_url, "fetched")
            pages.append(_page_result(page, fetch_status))
        for url, status in browser.page_status.items():
            if status != "fetched":
                errors.append({"source_url": url, "error": status})
    except Exception as error:
        errors.append(
            {"source_url": target["url"], "error": f"{type(error).__name__}: {error}"}
        )

    emails = sorted({value for page in pages for value in page["emails"]})
    linkedin = sorted({value for page in pages for value in page["linkedin"]})
    has_values = bool(emails or linkedin)
    fetched_pages = any(page["status"] == "fetched" for page in pages)
    if errors:
        status = "partial_error" if fetched_pages or has_values else "fetch_failed"
    elif not pages:
        status = "error"
        errors.append(
            {"source_url": target["url"], "error": "no page results returned"}
        )
    elif not has_values:
        status = "no_contacts" if fetched_pages else "fetch_failed"
    else:
        status = "partial_error" if not fetched_pages else "success"

    return {
        "name": target["name"],
        "url": target["url"],
        "reason": target["reason"],
        "status": status,
        "pages": pages,
        "errors": errors,
        "counts": {
            "pages": len(pages),
            "emails": len(emails),
            "linkedin": len(linkedin),
        },
        "emails": emails,
        "linkedin": linkedin,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--targets", type=Path, default=DEFAULT_TARGETS)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--depth", type=_nonnegative_int, default=1)
    parser.add_argument("--max-links", type=_positive_int, default=3)
    args = parser.parse_args()

    targets = _load_targets(args.targets)
    sites: list[dict[str, Any]] = []
    browser = _RecordingHttpxBrowser()
    with browser:
        for index, target in enumerate(targets):
            if index:
                time.sleep(SITE_DELAY_SECONDS)
            result = _extract_site(target, browser, args.depth, args.max_links)
            sites.append(result)
            counts = result["counts"]
            print(
                f"{result['name']}: {result['status']} — {counts['emails']} emails, "
                f"{counts['linkedin']} LinkedIn, {counts['pages']} pages"
            )

    summary = {
        "sites": len(sites),
        "success": sum(site["status"] == "success" for site in sites),
        "no_contacts": sum(site["status"] == "no_contacts" for site in sites),
        "failed": sum(site["status"] in {"error", "fetch_failed"} for site in sites),
        "partial_error": sum(site["status"] == "partial_error" for site in sites),
        "emails": len({email for site in sites for email in site["emails"]}),
        "linkedin": len({url for site in sites for url in site["linkedin"]}),
    }
    args.output.write_text(
        json.dumps({"summary": summary, "sites": sites}, indent=2, sort_keys=True)
        + "\n",
        encoding="utf-8",
    )
    print(f"Results written to {args.output}")


if __name__ == "__main__":
    main()
