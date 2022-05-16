import csv

from pathlib import Path
from typing import Any
from typing import Dict
from typing import List

from extract_emails.models import PageData

from .data_saver import DataSaver


class CsvSaver(DataSaver):
    def __init__(self, save_mode="w", **kwargs):
        super().__init__(**kwargs)
        self.save_mode = save_mode
        self.output_path = kwargs.get("output_path")
        print(self.output_path)
        if self.output_path is None or not isinstance(self.output_path, Path):
            raise ValueError("output_path must be a Path object")

    def save(self, data: List[PageData]):
        processed_data = self.process_data(data)
        headers = self.get_headers(processed_data)
        is_new_file = not self.output_path.exists()

        with open(self.output_path, self.save_mode, encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=headers)
            if is_new_file:
                w.writeheader()
            w.writerows(processed_data)

    @staticmethod
    def process_data(data: List[PageData]) -> List[Dict[str, Any]]:
        processed_data = []
        for i in data:
            d = {"website": i.website, "page": i.page_url}
            for k, v in i.data.items():
                for item in v:
                    d[k] = item
            processed_data.append(d)
        return processed_data

    @staticmethod
    def get_headers(data: List[Dict[str, Any]]) -> List[str]:
        headers = []
        for i in data:
            headers.extend(list(i.keys()))
        return list(set(headers))
