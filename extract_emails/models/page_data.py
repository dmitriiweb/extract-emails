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

    Args:
        website (str): website address from where data
        page_url (str): Page URL from where data
        data (Optional[Dict[str, List[str]]]): Data from the page in format: { 'label': [data, data] }, default: {}
    """

    website: str
    page_url: str
    data: Optional[Dict[str, List[str]]] = Field(default_factory=dict)

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
