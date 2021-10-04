from typing import List

from extract_emails.data_extractors import EmailExtractor
from extract_emails.factories.base_factory import BaseFactory
from extract_emails.link_filters import DefaultLinkFilter


class DefaultFilterAndEmailFactory(BaseFactory):
    """Will initialize `DefaultLinkFilter` and `EmailExtractor`

    Args:
        website_url (str): website for scan, e.g. https://example.com
        browser (PageSourceGetter): browser to get page source by URL
        depth (Optional[int]): scan's depth, default 10. Defaults to None
        max_links_from_page (Optional[int]): how many links a script shall get from each page. Defaults to None

    Examples:
        >>> from extract_emails import DefaultFilterAndEmailFactory as Factory
        >>> from extract_emails import DefaultWorker
        >>> from extract_emails.browsers.requests_browser import RequestsBrowser as Browser
        >>>
        >>> browser = Browser()
        >>> url = 'https://en.wikipedia.org/'
        >>> factory = Factory(website_url=url, browser=browser)
        >>> worker = DefaultWorker(factory)
        >>> data = worker.get_data()
        >>> data
            [
                PageData(
                    website='https://en.wikipedia.org/',
                    page_url='https://en.wikipedia.org/Email_address',
                    data={'email': ['"John.Doe."@example.com', 'x@example.com']}
                ),
                PageData(
                    website='https://en.wikipedia.org/',
                    page_url='https://en.wikipedia.org/Email_address2',
                    data={'email': ['"John.Doe2."@example.com', 'x2@example.com']}
                ),
            ]

    """

    @property
    def link_filter(self) -> DefaultLinkFilter:
        """Initialize `DefaultLinkFilter`"""
        return DefaultLinkFilter(self.website_url)

    @property
    def data_extractors(self) -> List[EmailExtractor]:
        """Initialize `EmailExtractor`"""
        return [EmailExtractor()]
