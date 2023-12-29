# Intro

There are several main parts in the framework:

 - **browser** - Class to navigate through specific website and extract data from the webpages (*requests*, *selenium* etc.)
 - **link filter** - Class to extract URLs from a page corresponding to the website. There are two link filters:
     - [`DefaultLinkFilter`][extract_emails.link_filters.default_link_filter.DefaultLinkFilter] - Will extract all URLs corresponding to the website
     - [`ContactInfoLinkFilter`][extract_emails.link_filters.contact_link_filter.ContactInfoLinkFilter] - Will extract only contact URLs, e.g. */contact/*, */about-us/* etc
 - **data extractor** - Class to extract data from a page. At the moment there are two data extractors:
     - [`EmailExtractor`][extract_emails.data_extractors.email_extractor.EmailExtractor] - Will extract all emails from the page
     - [`LinkedinExtractor`][extract_emails.data_extractors.linkedin_extractor.LinkedinExtractor] - Will extract all links to Linkedin profiles from the page
 - **factories** - Combination of different *link filters* and *data extractors*, e.g. [`DefaultFilterAndEmailFactory`][extract_emails.factories.default_filter_and_email.DefaultFilterAndEmailFactory]
 or [`ContactFilterAndEmailAndLinkedinFactory`][extract_emails.factories.contact_filter_and_email_and_linkedin.ContactFilterAndEmailAndLinkedinFactory]
 - [`DefaultWorker`][extract_emails.workers.default_worker.DefaultWorker] - All data extractions goes here
## Installation
```bash
pip install extract_emails[all]
# or
pip install extract_emails[requests]
# or
pip install extract_emails[selenium]
```
## Simple Usage:
### As library
```python
from pathlib import Path

from extract_emails import DefaultFilterAndEmailFactory as Factory
from extract_emails import DefaultWorker
from extract_emails.browsers.requests_browser import RequestsBrowser as Browser
from extract_emails.data_savers import CsvSaver


websites = [
    "website1.com",
    "website2.com",
]

browser = Browser()
data_saver = CsvSaver(save_mode="a", output_path=Path("output.csv"))

for website in websites:
    factory = Factory(
        website_url=website, browser=browser, depth=5, max_links_from_page=1
    )
    worker = DefaultWorker(factory)
    data = worker.get_data()
    data_saver.save(data)
```
### As CLI tool
```bash
$ extract-emails --help

$ extract-emails --url https://en.wikipedia.org/wiki/Email -of output.csv -d 1
$ cat output.csv
email,page,website
bob@b.org,https://en.wikipedia.org/wiki/Email,https://en.wikipedia.org/wiki/Email
```
