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
