# Save Data

Data store as [pydantic](https://pydantic-docs.helpmanual.io) models

## Save as CSV
```python
from extract_emails import DefaultFilterAndEmailFactory as Factory
from extract_emails.browsers.requests_browser import RequestsBrowser as Browser
from extract_emails.models import PageData
from extract_emails.workers import DefaultWorker


browser = Browser()
extractor = DefaultWorker("https://example.com", browser)
data = extractor.get_data()

PageData.save_as_csv(data, "output.csv")
# cat output.csv
website,page_url,email
https://example.com,https://example.com/about-us,email@example.com
https://example.com,https://example.com/about-us,email1@example.com
https://example.com,https://example.com/about-us,email2@example.com
https://example.com,https://example.com/about-us,email3@example.com

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
