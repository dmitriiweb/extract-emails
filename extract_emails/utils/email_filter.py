from typing import Iterable
from typing import Set

from ._top_level_domains import TOP_LEVEL_DOMAINS


def email_filter(emails: Iterable[str]) -> Set[str]:
    """Remove duplicated emails and strings looks like emails (2@pic.png)

    Examples:
        >>> from extract_emails.utils import email_filter
        >>> test_emails = ["email@email.com", "email@email.com", "2@pic.png"]
        >>> filtered_emails = email_filter(test_emails)
        >>> filtered_emails
        {"email@email.com"}

    Args:
        emails: List of new emails

    Returns:
        List of filtered emails
    """
    return set(
        email for email in emails if "." + email.split(".")[-1] in TOP_LEVEL_DOMAINS
    )
