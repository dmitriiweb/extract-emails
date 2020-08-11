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
        >>> extractor = EmailExtractor(website=['https://example.com'], chrome, depth=10, max_links_from_page=-1)
        >>> emails = extractor.get_emails()

    :param List[str] websites: List of URLs for scan
    :param browser: browser to get page source by URL
    :param int depth: scan's depth, default 10
    :param int max_links_from_page: how many links a script shall get from each page, default -1 (all)
    :param html_handler: handler to get emails and links from a page
    :param emails_filter: handler to remove duplicated emails, and etc.
    :param links_filter: handler to filter links from
    """

    def __init__(
        self,
        websites: List[str],
        browser: Type[BrowserInterface],
        depth: int = 10,
        max_links_from_page: int = -1,
        html_handler: Type[HTMLHandlerInterface] = DefaultHTMLHandler,
        emails_filter: Type[EmailFilterInterface] = EmailFilterInterface,
        links_filter: Type[LinkFilterInterface] = DefaultLinkFilter,
    ):
        self.websites = websites
        self.browser = browser
        self.depth = depth
        self.max_links_from_page = max_links_from_page
        self.html_handler = html_handler
        self.emails_filter = emails_filter
        self.links_filter = links_filter
