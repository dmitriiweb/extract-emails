import re
from bs4 import BeautifulSoup
from . import DataExtractor
from ..utils import email_filter


class AdvancedEmailExtractor(DataExtractor):
    def __init__(self):
        # Regex for standard and obfuscated emails
        self.email_pattern = re.compile(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
            re.IGNORECASE
        )

    @property
    def name(self) -> str:
        return "email"

    def preprocess(self, text: str) -> str:
        """Normalize common obfuscations to standard email format."""
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
        """Decode Cloudflare-protected email from data-cfemail attribute."""
        key = int(encoded[:2], 16)
        return "".join(
            chr(int(encoded[i:i+2], 16) ^ key) for i in range(2, len(encoded), 2)
        )

    def is_junk(self, email: str) -> bool:
        """Filter likely junk/system emails."""
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
        emails = set()

        # 1. Extract emails from normal text (with preprocessing)
        cleaned_text = self.preprocess(page_source)
        for match in self.email_pattern.findall(cleaned_text):
            if not self.is_junk(match):
                emails.add(match.lower())

        # 2. Extract Cloudflare-obfuscated emails
        soup = BeautifulSoup(page_source, "html.parser")
        cf_elements = soup.select("[data-cfemail]")
        for elem in cf_elements:
            encoded = str(elem.get("data-cfemail"))
            if encoded:
                decoded = self.cf_decode_email(encoded)
                if not self.is_junk(decoded):
                    emails.add(decoded.lower())

        return email_filter(emails)
