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
