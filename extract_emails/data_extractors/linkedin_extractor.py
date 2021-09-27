import re

from typing import Set

from extract_emails.data_extractors import DataExtractor


class LinkedinExtractor(DataExtractor):
    def __init__(self):
        self.regexp = re.compile(
            r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
        )

    @property
    def name(self) -> str:
        return "linkedin"

    def get_data(self, page_source: str) -> Set[str]:
        """Extract links to Linkedin profiles

        Args:
            page_source: webpage content

        Returns:
            Set of urls, e.g. {'https://www.linkedin.com/in/venjamin-brant-73381ujy3u'}
        """
        all_urls = self.regexp.findall(page_source)
        url_filter = "linkedin.com/in/"
        linkedin_urls = set([i[0] for i in all_urls if url_filter in i[0]])
        return linkedin_urls
