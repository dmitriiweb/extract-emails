from pprint import pprint

from extract_emails import DefaultFilterAndEmailFactory as Factory
from extract_emails.browsers import RequestsBrowser as Browser
from extract_emails.workers import DefaultWorker


browser = Browser()
url = "https://en.wikipedia.org/wiki/Email_address"
factory = Factory(website_url=url, browser=browser, depth=0, max_links_from_page=0)
extractor = DefaultWorker(factory)
pprint(extractor.get_data())
