#!/usr/local/bin/python3
# -*- coding: utf-8
from typing import List, Type, Optional

from extract_emails.browsers import RequestsBrowser, BrowserInterface
from extract_emails.html_handlers import HTMLHandlerInterface, DefaultHTMLHandler
from extract_emails.email_filters import EmailFilterInterface, DefaultEmailFilter
from extract_emails.link_filters import LinkFilterInterface, DefaultLinkFilter


class EmailExtractor:
    """
    Extract emails from a website

    Example:
        >>> extractor = EmailExtractor(browser, depth=10, max_links_from_page=-1)
        >>> emails = extractor.get_emails()

    :param str website_url: website for scan, e.g. https://example.com
    :param browser: browser to get page source by URL
    :param int depth: scan's depth, default 10
    :param int max_links_from_page: how many links a script shall get from each page, default -1 (all)
    """

    def __init__(
        self,
        website_url: str,
        browser: Type[BrowserInterface],
        depth: int = 10,
        max_links_from_page: int = -1,
    ):
        self.website = website_url
        self.browser = browser
        self.depth = depth
        self.max_links_from_page = max_links_from_page

        self._links: List[str] = []
        self._emails: List[str] = []
        self._current_depth: int = 0

        self.html_handler = DefaultHTMLHandler()
        self.links_filter = DefaultLinkFilter(self.website)
        self.emails_filter = DefaultEmailFilter()

    def get_emails(self):
        """Extract emails from webpages
        """
        url = self._get_url()
        page_source = self.browser.get_page_source(url)

        links = self.html_handler.get_links(page_source)
        emails = self.html_handler.get_emails(page_source)

        filtered_links = self.links_filter.filter(links)
        filtered_emails = self.emails_filter.filter(emails)

    def _get_url(self) -> Optional[str]:
        if self._current_depth == 0:
            return self.website
        try:
            return self._links.pop(0)
        except IndexError:
            return None
