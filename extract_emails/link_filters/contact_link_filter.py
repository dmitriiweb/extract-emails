from typing import Iterable
from typing import List
from typing import Optional
from typing import Set
from urllib.parse import urljoin

from extract_emails.link_filters.link_filter_base import LinkFilterBase


class ContactInfoLinkFilter(LinkFilterBase):
    """Contact information filter for links.

    Only keep the links might contain the contact information.

    Examples:
        >>> from extract_emails.link_filters import ContactInfoLinkFilter
        >>> link_filter = ContactInfoLinkFilter("https://example.com")
        >>> filtered_links = link_filter.filter(['/about-us', '/search'])
        >>> filtered_links
        ['https://example.com/about-us']


        >>> from extract_emails.link_filters import ContactInfoLinkFilter
        >>> link_filter = ContactInfoLinkFilter("https://example.com", use_default=True)
        >>> filtered_links = link_filter.filter(['/blog', '/search'])
        >>> filtered_links
        ['https://example.com/blog', 'https://example.com/search']

        >>> from extract_emails.link_filters import ContactInfoLinkFilter
        >>> link_filter = ContactInfoLinkFilter("https://example.com", use_default=False)
        >>> filtered_links = link_filter.filter(['/blog', '/search'])
        >>> filtered_links
        []

        >>> from extract_emails.link_filters import ContactInfoLinkFilter
        >>> link_filter = ContactInfoLinkFilter("https://example.com", contruct_candidates=['search'])
        >>> filtered_links = link_filter.filter(['/blog', '/search'])
        >>> filtered_links
        ['https://example.com/search']
    """

    default_contruct_candidates = [
        "about",
        "about-us",
        "aboutus",
        "contact",
        "contact-us",
        "contactus",
    ]

    checked_links: Set[str] = set()

    def __init__(
        self,
        website: str,
        contruct_candidates: Optional[List[str]] = None,
        use_default: bool = True,
    ):
        """

        Args:
            website: website address (scheme and domain), e.g. https://example.com
            contruct_candidates: keywords for filtering the list of URLs,
                default: see `self.default_contruct_candidates`
            use_default:  if no contactinfo urls found and return filtered_urls,
                default: True
        """
        super().__init__(website)
        self.candidates = (
            contruct_candidates
            if contruct_candidates is not None
            else self.default_contruct_candidates
        )
        self.use_default = use_default

    def filter(self, urls: Iterable[str]) -> Set[str]:
        """Filter out the links without keywords

        Args:
            urls: List of URLs for filtering

        Returns:
            List of filtered URLs
        """
        filtered_urls = set()
        contactinfo_urls = set()

        for url in urls:
            url = urljoin(self.website, url)

            if not url.startswith(self.website):
                continue
            filtered_urls.add(url)

            for cand in self.candidates:
                if cand in url.lower():
                    contactinfo_urls.add(url)
                    break

        return (
            filtered_urls
            if len(contactinfo_urls) == 0 and self.use_default
            else contactinfo_urls
        )
