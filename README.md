# Extract Emails

![Image](https://github.com/dmitriiweb/extract-emails/blob/docs_improvements/images/email.png?raw=true)

[![PyPI version](https://badge.fury.io/py/extract-emails.svg)](https://badge.fury.io/py/extract-emails)

Extract emails and linkedins profiles from a given website

[Documentation](https://dmitriiweb.github.io/extract-emails/)

## Requirements

- Python >= 3.10

## Installation

```bash
# Install the backend you need; HTTPX and Playwright are independent extras.
pip install "extract-emails[httpx]"
# Or, for Chromium:
pip install "extract-emails[playwright]"
playwright install chromium --with-deps
# Install both optional backends only if you need both:
pip install "extract-emails[all]"
```

## Quick Usage

### As a library

The HTTPX backend supports synchronous and asynchronous extraction. Substitute a
URL for a site you are authorized to crawl (a local test server is suitable).
Each function owns and closes its browser; call the function you need.

```python
from pathlib import Path

from extract_emails import DefaultWorker
from extract_emails.browsers import HttpxBrowser
from extract_emails.models import PageData


def run_sync(url: str) -> None:
    with HttpxBrowser() as browser:
        worker = DefaultWorker(url, browser)
        data = worker.get_data()
    PageData.to_csv(data, Path("output-sync.csv"))


async def run_async(url: str) -> None:
    async with HttpxBrowser() as browser:
        worker = DefaultWorker(url, browser)
        data = await worker.aget_data()
    await PageData.ato_csv(data, Path("output-async.csv"))


# Call one from your application, for example:
# run_sync("http://127.0.0.1:8000/")
# In an async function: await run_async("http://127.0.0.1:8000/")
```

Install only the browser backend you use: `pip install "extract-emails[httpx]"`
for HTTPX, or `pip install "extract-emails[playwright]"` followed by
`playwright install chromium --with-deps` for Chromium. The extras are
independent; installing one does not install the other. For Chromium, replace
`HttpxBrowser` with `ChromiumBrowser` in the corresponding sync or async
context manager and install the Playwright extra. Install both extras only if
you need both backends. `pip install "extract-emails[all]"` installs all extras.

### As CLI tool
```bash
$ extract-emails --help

$ extract-emails --url https://en.wikipedia.org/wiki/Email -of output.csv
$ cat output.csv
email,page,website
bob@b.org,https://en.wikipedia.org/wiki/Email,https://en.wikipedia.org/wiki/Email
```