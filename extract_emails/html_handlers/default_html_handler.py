from typing import List
import re

from .html_handler_interface import HTMLHandlerInterface


class DefaultHTMLHandler(HTMLHandlerInterface):
    def __init__(self):
        self.email_pattern = re.compile(r"\b[\w.-]+?@\w+?\.(?!jpg|png|jpeg)\w+?\b")
        self.link_pattern = re.compile(r'<a\s+(?:[^>]*?\s+)?href=(["\'])(.*?)\1')

    def get_emails(self, page_source: str) -> List[str]:
        """
        Extract all sequences similar to email

        :param str page_source: HTML page source
        :return: List of emails
        """
        return self.email_pattern.findall(page_source)

    def get_links(self, page_source: str) -> List[str]:
        """
        Extract all URLs corresponding to current website

        :param str page_source: HTML page source
        :return: List of URLs
        """
        links = self.link_pattern.findall(page_source)
        links = [x[1] for x in links]
        return links
