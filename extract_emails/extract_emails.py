#!/usr/local/bin/python3
# -*- coding: utf-8
from extract_emails.browsers import RequestsBrowser, BrowserInterface
from extract_emails.html_handlers import HTMLHandlerInterface, DefaultHTMLHandler
from extract_emails.email_filters import EmailFilterInterface, DefaultEmailFilter
from extract_emails.link_filters import LinkFilterInterface, DefaultLinkFilter


class EmailExtractor:
    """
    Extract emails from a website

    :param str website: website's URL
    :param int depth: scan's depth, default 10
    :param int max_links_from_page: how many links a script shall get from each page, default -1 (all)
    """
    browser: BrowserInterface = RequestsBrowser
    html_handler: HTMLHandlerInterface = DefaultHTMLHandler
    emails_filter: EmailFilterInterface = DefaultEmailFilter
    links_filter: LinkFilterInterface = DefaultLinkFilter

    _current_depth: int = 0

    def __init__(self, website: str, depth: int = 10, max_links_from_page: int = -1):
        self.website = DefaultLinkFilter.get_website_address(website)
        self.depth = depth
        self.max_links_from_page = max_links_from_page
