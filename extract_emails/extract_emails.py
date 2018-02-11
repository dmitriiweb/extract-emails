import re
import requests
from lxml import html
from fake_useragent import UserAgent


class ExtractEmails:
    """
    Extract emails from a given website
    """
    ua = UserAgent()
    agents = {'ie': ua.ie, 'msie': ua.msie, 'opera': ua.opera,
              'chrome': ua.chrome, 'google': ua.google, 'firefox': ua.firefox,
              'safari': ua.safari, 'random': ua.random}

    def __init__(self, url, depth=None, print_log=False, ssl_verify=True, user_agent='random'):
        self.verify = ssl_verify
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
            'User-Agent': self.agents[user_agent]}
        self.extract_emails(url)

    def extract_emails(self, url):
        r = requests.get(url, headers=self.headers, verify=self.verify)
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
        emails = re.findall(r'\b[\w.-]+?@\w+?\.(?!jpg|png|jpeg)\w+?\b', page)
        if emails:
            for email in emails:
                if email not in self.emails:
                    self.emails.append(email)

    def get_all_links(self, page):
        tree = html.fromstring(page)
        all_links = tree.findall('.//a')
        for link in all_links:
            try:
                link_href = link.attrib['href']
                if link_href.startswith(self.url) or link_href.startswith('/'):
                    if link_href.startswith('/'):
                        link_href = self.url + link_href
                    if link_href not in self.for_scan:
                        self.for_scan.append(link_href)
            except KeyError:
                pass


if __name__ == '__main__':
    em = ExtractEmails('http://www.cumberlandhomes.org', print_log=True, depth=20, ssl_verify=False, user_agent='random')
    print(em.emails)
