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

## Simple Usage:
### As library
```python
from extract_emails.browsers.requests_browser import RequestsBrowser as Browser
from extract_emails import DefaultFilterAndEmailFactory as Factory
from extract_emails import DefaultWorker

browser = Browser()
url = 'https://en.wikipedia.org/'
factory = Factory(website_url=url, browser=browser)
worker = DefaultWorker(factory)
data = worker.get_data()
print(data)
"""
[
    PageData(
        website='https://en.wikipedia.org/',
        page_url='https://en.wikipedia.org/Email_address',
        data={'email': ['"John.Doe."@example.com', 'x@example.com']}
    ),
    PageData(
        website='https://en.wikipedia.org/',
        page_url='https://en.wikipedia.org/Email_address2',
        data={'email': ['"John.Doe2."@example.com', 'x2@example.com']}
    ),
]
"""
```
### As CLI tool
```bash
$ extract-emails --help

$ extract-emails --url https://en.wikipedia.org/wiki/Email -of output.csv -d 1
$ cat output.csv
email,page,website
bob@b.org,https://en.wikipedia.org/wiki/Email,https://en.wikipedia.org/wiki/Email
```
