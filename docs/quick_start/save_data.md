# Save Data

## Save as CSV

`PageData.to_csv` and `PageData.ato_csv` append rows to a CSV file. The model
methods use `website` and `page_url` metadata columns. `CsvSaver` is a separate
API and uses `website` and `page`; its metadata spelling is intentionally
different.

```python
from pathlib import Path

from extract_emails import DefaultWorker
from extract_emails.browsers import HttpxBrowser
from extract_emails.models import PageData


def save_sync(url: str, output_path: Path) -> None:
    with HttpxBrowser() as browser:
        data = DefaultWorker(url, browser).get_data()
    PageData.to_csv(data, output_path)


async def save_async(url: str, output_path: Path) -> None:
    async with HttpxBrowser() as browser:
        data = await DefaultWorker(url, browser).aget_data()
    await PageData.ato_csv(data, output_path)


# save_sync("http://127.0.0.1:8000/", Path("output.csv"))
# From an async function:
# await save_async("http://127.0.0.1:8000/", Path("output.csv"))
```

The data columns are the union of labels in first-seen order. Values for each
label are written as independent columns and padded with blank cells to fit
the widest list on that page; the CSV does not imply a relationship between,
for example, an email and a LinkedIn URL on the same row. Empty input is a
no-op. Appending to a nonempty file requires a matching header; a schema
mismatch raises `ValueError` before the file is changed. The model methods
append, so a new file receives a header and an existing compatible file keeps
its existing header.

Extraction labels that match a metadata column, including labels prefixed by
one or more `data.` segments, are written with one additional `data.` prefix.
For example, model data labeled `website` is exported as `data.website`, and
`data.website` as `data.data.website`; saver metadata collisions follow the
same rule for its `website` and `page` columns.

Example CSV output (shown as data, not Python):

```csv
website,page_url,email,linkedin
https://example.com,https://example.com/about,email@example.com,https://linkedin.com/in/example
```

## Crawl and browser behavior

The seed page is at crawl distance 0; `depth` is the maximum link distance
included. `max_links_from_page` limits outgoing links per page, while `0`
means unlimited. Negative depth or link limits raise `ValueError`. A
`DefaultWorker` is single-use; create a new worker for another crawl.

Both browser context managers support idempotent `stop()` calls, including
before startup. Starting an already active browser raises `RuntimeError`.
Startup failures roll back resources already acquired, and shutdown attempts
all cleanup steps. Expected network/navigation failures return an empty string;
HTTPX error status responses do as well. Programming and lifecycle errors
propagate. Chromium continues to wait for `networkidle`; this default has not
been changed, and no performance improvement is claimed.
