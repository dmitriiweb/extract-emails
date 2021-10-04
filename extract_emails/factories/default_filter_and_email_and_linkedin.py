from typing import List
from typing import Union

from extract_emails.data_extractors import EmailExtractor
from extract_emails.data_extractors import LinkedinExtractor
from extract_emails.factories.base_factory import BaseFactory
from extract_emails.link_filters import DefaultLinkFilter


class DefaultFilterAndEmailAndLinkedinFactory(BaseFactory):
    """Will initialize `DefaultLinkFilter` and `EmailExtractor` and `LinkedinExtractor`

    Args:
        website_url (str): website for scan, e.g. https://example.com
        browser (PageSourceGetter): browser to get page source by URL
        depth (Optional[int]): scan's depth, default 10. Defaults to None
        max_links_from_page (Optional[int]): how many links a script shall get from each page. Defaults to None

    Examples:
        >>> from extract_emails import DefaultFilterAndEmailAndLinkedinFactory as Factory
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
                    data={
                    'email': ['"John.Doe."@example.com', 'x@example.com'],
                    'linkedin': ['linkedin_url1', 'linkedin_url2'],
                    }
                ),
                PageData(
                    website='https://en.wikipedia.org/',
                    page_url='https://en.wikipedia.org/Email_address2',
                    data={
                    'email': ['"John.Doe."@example.com', 'x@example.com'],
                    'linkedin': ['linkedin_url3', 'linkedin_url4'],
                    }
                ),
            ]

    """

    @property
    def link_filter(self) -> DefaultLinkFilter:
        """Initialize `DefaultLinkFilter`"""
        return DefaultLinkFilter(self.website_url)

    @property
    def data_extractors(self) -> List[Union[EmailExtractor, LinkedinExtractor]]:
        """Initialize `EmailExtractor` and `LinkedinExtractor`"""
        return [EmailExtractor()]
