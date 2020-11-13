from typing import List
import re

from .html_handler_interface import HTMLHandlerInterface


class DefaultHTMLHandler(HTMLHandlerInterface):
    def __init__(self):
        # regexp source: https://emailregex.com/
        self.email_pattern = re.compile(
            r"""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""
        )
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
