from typing import Iterable
from typing import List
from typing import Optional
from typing import Set
from urllib.parse import urljoin
from urllib.parse import urlparse

from extract_emails.link_filters.link_filter_base import LinkFilterBase


class ContactInfoLinkFilter(LinkFilterBase):
    """
    Contact information filter for links.
    Filter out the links without ['about', 'contact', 'about-us', 'contact-us', ... ].
    Only keep the links might contain the contact information.

    :param list(str) links: List of URLs
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
        # no contactinfo urls found and return filtered_urls
        super().__init__(website)
        self.candidates = (
            contruct_candidates
            if contruct_candidates is not None
            else self.default_contruct_candidates
        )
        self.use_default = use_default

    def filter(self, links: Iterable[str]) -> Set[str]:
        filtered_urls = set()
        contactinfo_urls = set()

        for url in links:
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
