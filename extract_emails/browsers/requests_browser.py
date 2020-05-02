from typing import Optional, Dict
import requests

from .browser_interface import BrowserInterface


class RequestsBrowser(BrowserInterface):
    """
    RequestsBrowser
    ----------------
    Make GET requests via requests library

    **Example:**
    ::

        browser = RequestsBrowser()
        browser.open()
        page_source = browser.get_page_source('https://example.com')
    """

    def __init__(self):
        self._session = None

    def open(self):
        """Create requests.Session() object"""
        self._session = requests.Session()

    def close(self):
        pass

    def _get(self, url: str, headers: Optional[Dict[str, str]]) -> str:
        try:
            r = self._session.get(url, headers=headers, timeout=1).text
        except:
            r = ''
        return r

    def get_page_source(self, url: str, headers: Optional[Dict[str, str]] = None) -> str:
        """
        Return page source from url

        :param str url: page url
        :param dict headers: headers for GET request, default: None
        :return: str, HTML from page

        **Example**:
        ::

            url = 'https://example.com'
            headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P)'}
            page_source = browser.get_page_source(url, headers)
        """
        response = self._get(url, headers)
        return response
