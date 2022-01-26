# Extract Emails

![Image](https://github.com/dmitriiweb/extract-emails/blob/docs_improvements/images/email.png?raw=true)

[![PyPI version](https://badge.fury.io/py/extract-emails.svg)](https://badge.fury.io/py/extract-emails)

Extract emails and linkedins profiles from a given website

**Support the project with BTC**: *bc1q0cxl5j3se0ufhr96h8x0zs8nz4t7h6krrxkd6l*

[Documentation](https://dmitriiweb.github.io/extract-emails/)

## Requirements
- Python >= 3.7

## Installation
```
pip install extract_emails
```

## Simple Usage
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
