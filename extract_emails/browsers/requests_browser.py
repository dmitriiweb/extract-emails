from typing import Any
from typing import Dict

import requests

from loguru import logger

from extract_emails.browsers.page_source_getter import PageSourceGetter


class RequestsBrowser(PageSourceGetter):
    """Wrapper on requests library

    Examples:
        >>> from extract_emails.browsers.requests_browser import RequestsBrowser
        >>> browser = RequestsBrowser()
        >>> page_source = browser.get_page_source('https://example.com')
    """

    requests_timeout = 0.05

    def __init__(self, headers: Dict[str, Any] = None):
        """

        Args:
            headers: headers for requests
        """
        self.headers = headers
        self.session = requests.Session()

    def get_page_source(self, url: str) -> str:
        """Get page source text from URL

        Args:
            url: URL

        Returns:
            page source as text
        """
        try:
            response = requests.get(url, headers=self.headers)
        except Exception as e:
            logger.error(f"Could not get page source from {url}: {e}")
            return ""
        return response.text
