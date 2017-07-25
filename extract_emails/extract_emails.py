import re
import requests
from bs4 import BeautifulSoup as BSoup


class ExtractEmails:
    """
    Extract emails from a given website
    """

    def __init__(self, url, depth=None, print_log=False):
        if url.endswith('/'):
            self.url = url[:-1]
        else:
            self.url = url
        self.print_log = print_log
        self.depth = depth
        self.scanned = []
        self.for_scan = []
        self.emails = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.112 Safari/537.36 Vivaldi/1.91.867.48'}
        self.extract_emails(url)

    def extract_emails(self, url):
        r = requests.get(url, headers=self.headers)
        self.scanned.append(url)
        if r.status_code == 200:
            self.get_all_links(r.text)
            self.get_emails(r.text)
        if self.print_log:
            self.print_logs()
        for new_url in self.for_scan[:self.depth]:
            if new_url not in self.scanned:
                self.extract_emails(new_url)

    def print_logs(self):
        print('URLs: {}, emails: {}'
              .format(len(self.scanned), len(self.emails)))

    def get_emails(self, page):
        emails = re.findall(r'\b[\w.-]+?@\w+?\.\w+?\b', page)
        if emails:
            for email in emails:
                if email not in self.emails:
                    self.emails.append(email)

    def get_all_links(self, page):
        bs_obj = BSoup(page, 'html.parser')
        all_links = bs_obj.find_all('a')
        for link in all_links:
            try:
                link_href = link['href']
                if link_href.startswith(self.url) or link_href.startswith('/'):
                    if link_href.startswith('/'):
                        link_href = self.url + link_href
                    if link_href not in self.for_scan:
                        self.for_scan.append(link_href)
            except KeyError:
                pass


if __name__ == '__main__':
    em = ExtractEmails('https://www.fortress.com/', print_log=True, depth=20)
    print(em.emails)
