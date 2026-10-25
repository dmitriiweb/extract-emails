from __future__ import annotations

import csv
from itertools import zip_longest
from pathlib import Path
from typing import TYPE_CHECKING, Iterable, Iterator, NamedTuple, Sequence

import aiofiles
from aiocsv import AsyncReader

if TYPE_CHECKING:
    from .page_data import PageData


class CsvSchema(NamedTuple):
    headers: list[str]
    columns: list[tuple[str, str]]


def csv_schema(
    pages: Iterable[PageData], metadata_headers: tuple[str, ...]
) -> CsvSchema:
    """Build a stable mapping from raw extraction labels to CSV columns."""
    labels = []
    seen = set()
    for page in pages:
        for label in page.data:
            if label not in seen:
                labels.append(label)
                seen.add(label)

    columns = []
    for label in labels:
        base = label
        while base.startswith("data."):
            base = base.removeprefix("data.")
        output = f"data.{label}" if base in metadata_headers else label
        columns.append((label, output))

    headers = [*metadata_headers, *(output for _, output in columns)]
    return CsvSchema(headers, columns)


def iter_csv_rows(
    pages: Sequence[PageData],
    metadata_headers: tuple[str, ...],
    schema: CsvSchema | None = None,
) -> Iterator[dict[str, str]]:
    """Yield wide CSV rows, padding independent value lists with blanks."""
    if schema is None:
        schema = csv_schema(pages, metadata_headers)
    raw_labels = tuple(raw for raw, _ in schema.columns)
    output_labels = tuple(output for _, output in schema.columns)
    for page in pages:
        values = (page.data.get(label, []) for label in raw_labels)
        for row_values in zip_longest(*values, fillvalue=""):
            row = {
                metadata_headers[0]: page.website,
                metadata_headers[1]: page.page_url,
            }
            row.update(zip(output_labels, row_values, strict=True))
            yield row


def validate_append_header(filepath: Path, headers: list[str]) -> None:
    """Reject appending rows whose schema differs from an existing CSV."""
    if not filepath.exists() or not filepath.stat().st_size:
        return
    with open(filepath, "r", encoding="utf-8", newline="") as existing:
        existing_headers = next(csv.reader(existing), [])
    if existing_headers != headers:
        raise ValueError(
            f"CSV header mismatch: existing {existing_headers!r}, requested {headers!r}"
        )


async def avalidate_append_header(filepath: Path, headers: list[str]) -> None:
    """Asynchronously reject appends with a different existing CSV schema."""
    if not filepath.exists() or not filepath.stat().st_size:
        return
    async with aiofiles.open(filepath, "r", encoding="utf-8", newline="") as existing:
        reader = AsyncReader(existing)
        iterator = reader.__aiter__()
        try:
            existing_headers = await iterator.__anext__()
        except StopAsyncIteration:
            existing_headers = []
    if existing_headers != headers:
        raise ValueError(
            f"CSV header mismatch: existing {existing_headers!r}, requested {headers!r}"
        )
