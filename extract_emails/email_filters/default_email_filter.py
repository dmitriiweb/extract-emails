from typing import List

from extract_emails.email_filters import EmailFilterInterface


class DefaultEmailFilter(EmailFilterInterface):
    """
    Default email filter

    :param list(str) emails_list: list of emails from a page
    :param list(str) forbidden_emails: list of emails to exclude from a result
    """
    def __init__(self, emails_list: List[str], forbidden_emails: List[str] = ['example@example.com']):
        super(DefaultEmailFilter, self).__init__(emails_list)
        self.forbidden_emails = forbidden_emails
