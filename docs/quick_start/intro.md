# Intro

## Installation
```bash
pip install extract_emails[all]
# or
pip install extract_emails[httpx]
# or
pip install extract_emails[playwright]
```

## Quick Usage
### As library

```python
from pathlib import Path

from extract_emails import DefaultWorker
from extract_emails.browsers import ChromiumBrowser, HttpxBrowser
from extract_emails.models import PageData

def main():
    with ChromiumBrowser() as browser:
        worker = DefaultWorker("https://example.com, browser)
        data = worker.get_data()
        PageData.to_csv(data, Path("output.csv"))

    with HttpxBrowser() as browser:
        worker = DefaultWorker("https://example.com, browser)
        data = worker.get_data()
        PageData.to_csv(data, Path("output.csv"))

async def main():
    async with ChromiumBrowser() as browser:
        worker = DefaultWorker("https://example.com, browser)
        data = await worker.aget_data()
        await PageData.to_csv(data, Path("output.csv"))

    async with HttpxBrowser() as browser:
        worker = DefaultWorker("https://example.com, browser)
        data = await worker.aget_data()
        await PageData.to_csv(data, Path("output.csv"))

```
### As CLI tool
```bash
$ extract-emails --help

$ extract-emails --url https://en.wikipedia.org/wiki/Email -of output.csv
$ cat output.csv
email,page,website
bob@b.org,https://en.wikipedia.org/wiki/Email,https://en.wikipedia.org/wiki/Email
```
There are several main parts in the framework:

 - **browser** - Class to navigate through specific website and extract data from the webpages (*httpx*, *playwright* etc.)
 - **link filter** - Class to extract URLs from a page corresponding to the website. There are two link filters (`ContactInfoLinkFilter` by default):
     - [`DefaultLinkFilter`][extract_emails.link_filters.default_link_filter.DefaultLinkFilter] - Will extract all URLs corresponding to the website
     - [`ContactInfoLinkFilter`][extract_emails.link_filters.contact_link_filter.ContactInfoLinkFilter] - Will extract only contact URLs, e.g. */contact/*, */about-us/* etc
 - **data extractor** - Class to extract data from a page. At the moment there are two data extractors (both by default):
     - [`EmailExtractor`][extract_emails.data_extractors.email_extractor.EmailExtractor] - Will extract all emails from the page
     - [`LinkedinExtractor`][extract_emails.data_extractors.linkedin_extractor.LinkedinExtractor] - Will extract all links to Linkedin profiles from the page
 - [`DefaultWorker`][extract_emails.workers.default_worker.DefaultWorker] - All data extractions goes here