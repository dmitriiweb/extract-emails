# Extract Emails

![Image](https://github.com/dmitriiweb/extract-emails/blob/docs_improvements/images/email.png?raw=true)

[![PyPI version](https://badge.fury.io/py/extract-emails.svg)](https://badge.fury.io/py/extract-emails)

Extract emails and linkedins profiles from a given website

[Documentation](https://dmitriiweb.github.io/extract-emails/)

## Requirements

- Python >= 3.10

## Installation

```bash
pip install extract_emails[all]
# or
pip install extract_emails[httpx]
# or
pip install extract_emails[playwright]
playwright install chromium --with-deps
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