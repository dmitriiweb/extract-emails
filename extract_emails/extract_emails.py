import pickle
import os
import time

import re
import requests
from lxml import html

BASEDIR = os.path.dirname(os.path.abspath(__file__))
DOMAINS_FAIL = os.path.join(BASEDIR, 'top_level_domains.pkl')


class ExtractEmails:
    """
    Extract emails from a given website
    """

    def __init__(self, url: str, depth: int=None, print_log: bool=False, ssl_verify: bool=True, user_agent: str=None, request_delay: float=0):
        self.delay = request_delay
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
        self.headers = {'User-Agent': user_agent}
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
                time.sleep(self.delay)
                self.extract_emails(new_url)

    def print_logs(self):
        print('URLs: {}, emails: {}'
              .format(len(self.scanned), len(self.emails)))

    def get_emails(self, page):
        emails = re.findall(r'\b[\w.-]+?@\w+?\.(?!jpg|png|jpeg)\w+?\b', page)
        emails = [x.lower() for x in emails]
        domains = self.get_domains()
        emails = [x for x in emails if '.' + x.split('.')[-1] in domains]
        if emails:
            for email in emails:
                if email not in self.emails:
                    self.emails.append(email)

    def get_domains(self):
        with open(DOMAINS_FAIL, 'rb') as f:
            domains = pickle.load(f)
        return domains

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
    em = ExtractEmails('http://www.ThreeVillagePodiatry.com', print_log=True, user_agent='Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0',
                       depth=10)
    print(em.emails)
