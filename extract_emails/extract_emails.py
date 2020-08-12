#!/usr/local/bin/python3
# -*- coding: utf-8
from typing import List, Type

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

    :param browser: browser to get page source by URL
    :param int depth: scan's depth, default 10
    :param int max_links_from_page: how many links a script shall get from each page, default -1 (all)
    """

    html_handler: Type[HTMLHandlerInterface] = DefaultHTMLHandler
    emails_filter: Type[EmailFilterInterface] = DefaultEmailFilter
    links_filter: Type[LinkFilterInterface] = DefaultLinkFilter

    def __init__(
        self,
        browser: Type[BrowserInterface],
        depth: int = 10,
        max_links_from_page: int = -1,
    ):
        self.browser = browser
        self.depth = depth
        self.max_links_from_page = max_links_from_page

        self._links: List[str] = []
        self._emails: List[str] = []
        self._current_depth: int = 0

    def get_emails(self, website_url: str):
        """Extract emails from webpages
        """
        page_source = self.browser.get_page_source(website_url)

        html_handler = self.html_handler()
        links = html_handler.get_links(page_source)
        emails = html_handler.get_emails(page_source)
