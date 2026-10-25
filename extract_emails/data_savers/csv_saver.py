import csv
from pathlib import Path
from typing import Any, Iterable

from extract_emails.models import PageData
from extract_emails.models._csv import (
    csv_schema,
    iter_csv_rows,
    validate_append_header,
)

from .data_saver import DataSaver


class CsvSaver(DataSaver):
    def __init__(self, save_mode: str = "w", **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.save_mode = save_mode
        output_path = kwargs.get("output_path")
        if not isinstance(output_path, Path):
            raise ValueError("output_path must be a Path object")
        self.output_path: Path = output_path

    def save(self, data: Iterable[PageData]) -> None:
        pages = list(data)
        if not pages:
            return

        metadata = ("website", "page")
        schema = csv_schema(pages, metadata)
        append_mode = "a" in self.save_mode
        if append_mode:
            validate_append_header(self.output_path, schema.headers)

        write_header = ("w" in self.save_mode or "x" in self.save_mode) or (
            append_mode
            and (not self.output_path.exists() or self.output_path.stat().st_size == 0)
        )
        with open(self.output_path, self.save_mode, encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=schema.headers)
            if write_header:
                writer.writeheader()
            writer.writerows(iter_csv_rows(pages, metadata, schema))

    @staticmethod
    def process_data(data: Iterable[PageData]) -> list[dict[str, Any]]:
        pages = list(data)
        return list(iter_csv_rows(pages, ("website", "page")))

    @staticmethod
    def get_headers(data: Iterable[dict[str, Any]]) -> list[str]:
        headers = []
        seen = set()
        for row in data:
            for key in row:
                if key not in seen:
                    headers.append(key)
                    seen.add(key)
        return headers
