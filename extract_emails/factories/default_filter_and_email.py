from typing import List

from extract_emails.data_extractors import EmailExtractor
from extract_emails.factories.base_factory import BaseFactory
from extract_emails.link_filters import DefaultLinkFilter


class DefaultFilterAndEmailFactory(BaseFactory):
    """Will initialize `DefaultLinkFilter and EmailExtractor"""

    @property
    def link_filter(self) -> DefaultLinkFilter:
        """Initialize `DefaultLinkFilter`"""
        return DefaultLinkFilter(self.website_url)

    @property
    def data_extractors(self) -> List[EmailExtractor]:
        """Initialize `EmailExtractor`"""
        return [EmailExtractor()]
