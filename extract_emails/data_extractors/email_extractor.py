import re

from typing import Set

from extract_emails.data_extractors import DataExtractor
from extract_emails.utils import email_filter


class EmailExtractor(DataExtractor):
    def __init__(self):
        self.regexp = re.compile(
            r"""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""
        )

    @property
    def name(self) -> str:
        return "email"

    def get_data(self, page_source: str) -> Set[str]:
        """Extract emails from a string

        Args:
            page_source: webpage content

        Returns:
            Set of emails, e.g. {'email@email.com', 'email2@email.com'}
        """
        raw_emails = [i for i in self.regexp.findall(page_source)]
        return email_filter(raw_emails)
