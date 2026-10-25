import csv
from pathlib import Path

import aiofiles
from aiocsv import AsyncDictWriter
from pydantic import BaseModel, Field

from ._csv import (
    avalidate_append_header,
    csv_schema,
    iter_csv_rows,
    validate_append_header,
)


class PageData(BaseModel):
    """Representation for data from a webpage

    Examples:
        >>> from extract_emails.models import PageData
        >>> page_data = PageData(website='https://example.com', page_url='https://example.com/page123')

    Attributes:
        website (str): website address from where data
        page_url (str): Page URL from where data
        data (Optional[Dict[str, List[str]]]): Data from the page in format: { 'label': [data, data] }, default: {}
    """

    website: str
    page_url: str
    data: dict[str, list[str]] = Field(default_factory=dict)

    def __len__(self) -> int:
        if len(self.data) == 0:
            return 0
        return sum(len(i) for i in self.data.values())

    def append(self, label: str, vals: list[str]) -> None:
        """Append data from a page to the self.data collection

        Examples:
            >>> from extract_emails.models import PageData
            >>> page_data = PageData(website='https://example.com', page_url='https://example.com/page123')
            >>> page_data.append('email', ['email1@email.com', 'email2@email.com'])
            >>> page_data.page
            >>> {'email': ['email@email.com', 'email2@email.com']}

        Args:
            label: name of collection, e.g. email, linkedin
            vals: data from a page, e.g. emails, specific URLs etc.
        """
        try:
            self.data[label].extend(vals)
        except KeyError:
            self.data[label] = vals

    @classmethod
    def to_csv(cls, data: list["PageData"], filepath: Path) -> None:
        """Save list of `PageData` to CSV file

        Args:
            data: list of `PageData`
            filepath: path to a CSV file
        """
        if not data:
            return

        schema = csv_schema(data, ("website", "page_url"))
        validate_append_header(filepath, schema.headers)
        write_header = not filepath.exists() or filepath.stat().st_size == 0
        with open(filepath, "a", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=schema.headers)
            if write_header:
                writer.writeheader()
            writer.writerows(iter_csv_rows(data, ("website", "page_url"), schema))

    @classmethod
    async def ato_csv(cls, data: list["PageData"], filepath: Path) -> None:
        """Async save list of `PageData` to CSV file

        Args:
            data: list of `PageData`
            filepath: path to a CSV file
        """
        if not data:
            return

        schema = csv_schema(data, ("website", "page_url"))
        await avalidate_append_header(filepath, schema.headers)
        write_header = not filepath.exists() or filepath.stat().st_size == 0
        async with aiofiles.open(filepath, "a", encoding="utf-8", newline="") as f:
            writer = AsyncDictWriter(f, fieldnames=schema.headers)
            if write_header:
                await writer.writeheader()
            for row in iter_csv_rows(data, ("website", "page_url"), schema):
                await writer.writerow(row)
