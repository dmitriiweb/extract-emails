from pathlib import Path
from pprint import pprint
from typing import Any
from typing import Dict
from typing import List

from extract_emails.models import PageData

from .data_saver import DataSaver


class CsvSaver(DataSaver):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.output_path = kwargs.get("output_path")
        print(self.output_path)
        if self.output_path is None or not isinstance(self.output_path, Path):
            raise ValueError("output_path must be a Path object")

    def save(self, data: List[PageData]):
        processed_data = self.process_data(data)
        is_new_file = not self.output_path.exists()

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
