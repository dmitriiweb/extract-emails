from __future__ import annotations

import asyncio
from urllib.parse import urlsplit

import pytest

from extract_emails.link_filters import DefaultLinkFilter, LinkFilterBase
from extract_emails.workers import DefaultWorker

ROOT = "https://example.com/team/"


class FakeBrowser:
    def __init__(self, pages: dict[str, str], failures: set[str] | None = None):
        self.pages = pages
        self.failures = failures or set()
        self.requested: list[str] = []

    def get_page_source(self, url: str) -> str:
        self.requested.append(url)
        if url in self.failures:
            raise RuntimeError("page unavailable")
        return self.pages[url]

    async def aget_page_source(self, url: str) -> str:
        return self.get_page_source(url)


def _html(*hrefs: str) -> str:
    return "".join(f'<a href="{href}">link</a>' for href in hrefs)


def _worker(browser: FakeBrowser, *, depth: int = 2, limit: int = 20) -> DefaultWorker:
    return DefaultWorker(
        ROOT,
        browser,  # type: ignore[arg-type]
        link_filter=DefaultLinkFilter(ROOT),
        depth=depth,
        max_links_from_page=limit,
    )


def _run(worker: DefaultWorker, async_mode: bool) -> list[str]:
    if async_mode:
        pages = asyncio.run(worker.aget_data())
    else:
        pages = worker.get_data()
    return [page.page_url for page in pages]


@pytest.mark.parametrize("async_mode", [False, True])
def test_worker_depth_is_link_distance(async_mode: bool) -> None:
    pages = {
        ROOT: _html("a", "b"),
        ROOT + "a": _html("aa"),
        ROOT + "b": _html("bb"),
        ROOT + "aa": "",
        ROOT + "bb": "",
    }

    at_two = _run(_worker(FakeBrowser(pages), depth=2), async_mode)
    at_one = _run(_worker(FakeBrowser(pages), depth=1), async_mode)
    at_zero = _run(_worker(FakeBrowser(pages), depth=0), async_mode)

    assert set(at_two) == {ROOT, ROOT + "a", ROOT + "b", ROOT + "aa", ROOT + "bb"}
    assert set(at_one) == {ROOT, ROOT + "a", ROOT + "b"}
    assert at_zero == [ROOT]


@pytest.mark.parametrize("async_mode", [False, True])
def test_worker_schedules_cycles_and_diamond_nodes_once(async_mode: bool) -> None:
    pages = {
        ROOT: _html("a", "b", "#top"),
        ROOT + "a": _html("shared", "../team/"),
        ROOT + "b": _html("shared"),
        ROOT + "shared": "",
    }
    browser = FakeBrowser(pages)

    visited = _run(_worker(browser), async_mode)

    assert set(visited) == {ROOT, ROOT + "a", ROOT + "b", ROOT + "shared"}
    assert len(visited) == 4
    assert browser.requested.count(ROOT) == 1


@pytest.mark.parametrize("async_mode", [False, True])
def test_worker_handles_empty_discovery_and_failed_sibling(async_mode: bool) -> None:
    pages = {
        ROOT: _html("empty", "broken", "good"),
        ROOT + "empty": "",
        ROOT + "good": "",
    }
    browser = FakeBrowser(pages, failures={ROOT + "broken"})

    visited = _run(_worker(browser), async_mode)

    assert set(visited) == {ROOT, ROOT + "empty", ROOT + "good"}
    assert browser.requested == [ROOT, ROOT + "empty", ROOT + "broken", ROOT + "good"]


@pytest.mark.parametrize("async_mode", [False, True])
def test_worker_link_limit_and_zero_unlimited(async_mode: bool) -> None:
    pages = {
        ROOT: _html("first", "second", "third"),
        **{ROOT + name: "" for name in ("first", "second", "third")},
    }

    limited = _run(_worker(FakeBrowser(pages), limit=2), async_mode)
    unlimited = _run(_worker(FakeBrowser(pages), limit=0), async_mode)

    assert set(limited) == {ROOT, ROOT + "first", ROOT + "second"}
    assert set(unlimited) == {ROOT, ROOT + "first", ROOT + "second", ROOT + "third"}


@pytest.mark.parametrize("kwargs", [{"depth": -1}, {"limit": -1}])
def test_worker_rejects_negative_limits(kwargs: dict[str, int]) -> None:
    worker_kwargs = {"depth": 2, "limit": 20}
    worker_kwargs.update(kwargs)

    with pytest.raises(ValueError):
        _worker(FakeBrowser({ROOT: ""}), **worker_kwargs)


@pytest.mark.parametrize("async_mode", [False, True])
def test_worker_resolves_relative_links_and_filters_candidates(
    async_mode: bool,
) -> None:
    hrefs = (
        "contact",
        "../about#team",
        "mailto:hello@example.com",
        "javascript:void(0)",
        "https://other.example/contact",
        "#fragment",
    )
    pages = {
        ROOT: _html(*hrefs),
        ROOT + "contact": "",
        "https://example.com/about": "",
    }
    browser = FakeBrowser(pages)
    worker = _worker(browser)

    visited = _run(worker, async_mode)

    assert set(visited) == {ROOT, ROOT + "contact", "https://example.com/about"}
    assert all(urlsplit(url).scheme in {"http", "https"} for url in browser.requested)
    assert all("#" not in url for url in browser.requested)


@pytest.mark.parametrize("async_mode", [False, True])
def test_worker_resolves_relative_urls_from_nested_page(async_mode: bool) -> None:
    pages = {
        ROOT: _html("section/"),
        ROOT + "section/": _html("contact"),
        ROOT + "section/contact": "",
    }

    visited = _run(_worker(FakeBrowser(pages)), async_mode)

    assert set(visited) == {ROOT, ROOT + "section/", ROOT + "section/contact"}


def test_worker_link_filter_receives_resolved_fragment_free_urls() -> None:
    class RecordingFilter(DefaultLinkFilter):
        def __init__(self, website: str):
            super().__init__(website)
            self.received: list[str] = []

        def filter(self, urls):
            self.received.extend(urls)
            return super().filter(urls)

    browser = FakeBrowser(
        {ROOT: _html("child#section", "//example.com/other", "mailto:x@y.z")}
    )
    link_filter = RecordingFilter(ROOT)
    worker = DefaultWorker(ROOT, browser, link_filter=link_filter, depth=1)  # type: ignore[arg-type]

    _run(worker, False)

    assert link_filter.received == [ROOT + "child", "https://example.com/other"]


def test_worker_parser_handles_uppercase_and_unquoted_anchor_attributes() -> None:
    source = "<A HREF=https://example.com/contact>contact</A>"

    assert LinkFilterBase.get_links(source) == ["https://example.com/contact"]


@pytest.mark.parametrize("async_mode", [False, True])
def test_worker_does_not_schedule_origin_slash_as_duplicate_seed(
    async_mode: bool,
) -> None:
    root = "https://example.com"
    browser = FakeBrowser({root: _html("/")})
    worker = DefaultWorker(
        root,
        browser,  # type: ignore[arg-type]
        link_filter=DefaultLinkFilter(root),
        depth=1,
    )

    visited = _run(worker, async_mode)

    assert visited == [root]
    assert browser.requested == [root]


@pytest.mark.parametrize("async_mode", [False, True])
def test_worker_preserves_page_data_after_malformed_linkedin_candidate(
    async_mode: bool,
) -> None:
    pages = {
        ROOT: (
            "person@example.com https://[invalid/path "
            "https://LinkedIn.com/in/valid" + _html("contact")
        ),
        ROOT + "contact": "child@example.com",
    }
    worker = _worker(FakeBrowser(pages), depth=1)

    if async_mode:
        result = asyncio.run(worker.aget_data())
    else:
        result = worker.get_data()

    by_url = {page.page_url: page for page in result}
    assert set(by_url) == {ROOT, ROOT + "contact"}
    assert by_url[ROOT].data == {
        "email": ["person@example.com"],
        "linkedin": ["https://LinkedIn.com/in/valid"],
    }
    assert by_url[ROOT + "contact"].data["email"] == ["child@example.com"]
