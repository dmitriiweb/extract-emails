from typing import List
from typing import Set

from extract_emails.filters import EmailFilterInterface

from .domains import TOP_LEVEL_DOMAINS


class DefaultEmailFilter(EmailFilterInterface):
    """
    Default email filter

    """

    def __init__(self):
        self.checked_emails: Set[str] = set()

    def filter(self, emails: List[str]) -> List[str]:
        """
        Remove duplicates and filter by domain

        :param: list(str) emails: list of emails for filtering
        :return: List of emails
        """
        filtered_emails = []
        for email in emails:
            domain = "." + email.split(".")[-1]
            if domain not in TOP_LEVEL_DOMAINS:
                continue
            if email in self.checked_emails:
                continue
            self.checked_emails.add(email)
            filtered_emails.append(email)
        return filtered_emails
