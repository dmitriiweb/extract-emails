import re

from lxml import html

from ..utils import email_filter
from . import DataExtractor


class AdvancedEmailExtractor(DataExtractor):
    """Advanced email extractor with support for obfuscated and Cloudflare-protected emails."""

    def __init__(self):
        # Regex for standard and obfuscated emails
        self.email_pattern = re.compile(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", re.IGNORECASE
        )

    @property
    def name(self) -> str:
        """Name of the data extractor.

        Returns:
            "email"
        """
        return "email"

    def preprocess(self, text: str) -> str:
        """Normalize common obfuscations to standard email format.

        Replaces common email obfuscation patterns like "[at]", "(at)", " at " with "@"
        and "[dot]", "(dot)", " dot " with ".".

        Args:
            text: Text content that may contain obfuscated email addresses.

        Returns:
            Text with obfuscations normalized to standard email format.
        """
        replacements = [
            (r"\[\s*at\s*\]", "@"),
            (r"\(\s*at\s*\)", "@"),
            (r"\s+at\s+", "@"),
            (r"\[\s*dot\s*\]", "."),
            (r"\(\s*dot\s*\)", "."),
            (r"\s+dot\s+", "."),
        ]
        for pattern, repl in replacements:
            text = re.sub(pattern, repl, text, flags=re.IGNORECASE)
        return text

    def cf_decode_email(self, encoded: str) -> str:
        """Decode Cloudflare-protected email from data-cfemail attribute.

        Decodes email addresses that are obfuscated by Cloudflare's email protection
        feature using XOR encryption.

        Args:
            encoded: Hex-encoded email string from data-cfemail attribute.

        Returns:
            Decoded email address.
        """
        key = int(encoded[:2], 16)
        return "".join(
            chr(int(encoded[i : i + 2], 16) ^ key) for i in range(2, len(encoded), 2)
        )

    def is_junk(self, email: str) -> bool:
        """Filter likely junk/system emails.

        Checks if an email address appears to be a system or junk email based on
        various heuristics like length, hex patterns, and known junk domains.

        Args:
            email: Email address to check.

        Returns:
            True if the email appears to be junk, False otherwise.
        """
        local, domain = email.split("@", 1)
        if len(local) > 25:
            return True
        if re.fullmatch(r"[0-9a-f]{8,}", local):
            return True
        junk_domains = ("sentry.wixpress.com", "no-reply.github.com", "mailer-daemon")
        if domain.lower().endswith(junk_domains):
            return True
        return False

    def get_data(self, page_source: str) -> set[str]:
        """Extract emails from a webpage with support for obfuscated and protected emails.

        Extracts email addresses using multiple strategies:
        1. Regex matching on preprocessed text (handles common obfuscations)
        2. Decoding Cloudflare-protected emails from data-cfemail attributes

        Args:
            page_source: HTML webpage content.

        Returns:
            Set of extracted email addresses.
        """
        emails = set()

        # 1. Extract emails from normal text (with preprocessing)
        cleaned_text = self.preprocess(page_source)
        for match in self.email_pattern.findall(cleaned_text):
            if not self.is_junk(match):
                emails.add(match.lower())

        # 2. Extract Cloudflare-obfuscated emails
        doc = html.fromstring(page_source)
        cf_elements = doc.cssselect("[data-cfemail]")
        for elem in cf_elements:
            encoded = elem.get("data-cfemail")
            if encoded:
                decoded = self.cf_decode_email(encoded)
                if not self.is_junk(decoded):
                    emails.add(decoded.lower())

        return email_filter(emails)
