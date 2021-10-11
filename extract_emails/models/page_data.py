import csv

from itertools import zip_longest
from os import PathLike
from typing import Dict
from typing import List
from typing import Optional

from pydantic import BaseModel
from pydantic import Field


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
    data: Optional[Dict[str, List[str]]] = Field(default_factory=dict)

    def __len__(self) -> int:
        if len(self.data) == 0:
            return 0
        return sum(len(i) for i in self.data.values())

    def append(self, label: str, vals: List[str]) -> None:
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
    def save_as_csv(cls, data: List["PageData"], filepath: PathLike) -> None:
        """Save list of `PageData` to CSV file

        Args:
            data: list of `PageData`
            filepath: path to a CSV file
        """
        base_headers: List[str] = list(cls.schema()["properties"].keys())
        base_headers.remove("data")
        data_headers = [i for i in data[0].data.keys()]
        headers = base_headers + data_headers

        with open(filepath, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            for page in data:
                for data_in_row in zip_longest(*page.data.values()):
                    new_row = {"website": page.website, "page_url": page.page_url}
                    for counter, column in enumerate(data_headers):
                        new_row[column] = data_in_row[counter]

                    writer.writerow(new_row)
