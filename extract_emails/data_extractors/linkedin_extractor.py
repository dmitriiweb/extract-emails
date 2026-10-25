import re
from urllib.parse import urlsplit

from extract_emails.data_extractors import DataExtractor


class LinkedinExtractor(DataExtractor):
    def __init__(self):
        self.regexp = re.compile(
            r"""(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>\\'"]+|\(([^\s()<>\\'"]+|(\([^\s()<>\\'"]+\)))*\))+(?:\(([^\s()<>\\'"]+|(\([^\s()<>\\'"]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’\\]))"""
        )

    @property
    def name(self) -> str:
        return "linkedin"

    def get_data(self, page_source: str) -> set[str]:
        """Extract links to Linkedin profiles

        Args:
            page_source: webpage content

        Returns:
            Set of urls, e.g. {'https://www.linkedin.com/in/venjamin-brant-73381ujy3u'}
        """
        # Replace only complete delimiter entities; semicolonless query params stay intact.
        page_source = re.sub(
            r"&(?:quot|apos|lt|gt|#0*(?:34|39|60|62)|#x0*(?:22|27|3c|3e));",
            " ",
            page_source,
            flags=re.IGNORECASE,
        )
        all_urls = self.regexp.findall(page_source)
        linkedin_urls = set()
        for match in all_urls:
            url = re.sub(r"&amp;", "&", match[0], flags=re.IGNORECASE)
            try:
                parsed = urlsplit(url if "://" in url else f"https://{url}")
                hostname = (parsed.hostname or "").lower()
            except ValueError:
                continue
            if not (hostname == "linkedin.com" or hostname.endswith(".linkedin.com")):
                continue
            if parsed.path.startswith("/in/"):
                linkedin_urls.add(url)
        return linkedin_urls
