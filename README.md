# Extract Emails
Extract emails from a given website

## Requirements
- Python3
- requests
- lxml
- fake-useragent

## Installation
```
pip install extract_emails
```

## Usage
```
from extract_emails import ExtractEmails

em = ExtractEmails(url, depth=None, print_log=False, ssl_verify=True, user_agent=None, request_delay=0.0)
emails = em.emails
```
- *url*: str, ex: http://example.com
- *depth*: int, depth of scan
- *print_log*: boolean, print log or not
- *ssl_verify*: boolean
- *user_agent*: str
- *request_delay*: float

**ssl_verify** - use to avoid errors like this: *exceeded with url: /api/v1/pods?watch=False (Caused by SSLError(SSLError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:777)'),))*

**user_agent** - e.g. "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0"

**request_delay** - time delay between requests in seconds

**Return** list of emails.



## Changelog


#### Version 3.0.0
- Remove fake_useragent library
- Improve email extraction
- Add time delay between requests

#### Version 2.0.1
- Improved readme and setup files

#### Version 2.0.0

- Replaced BeautifulSoup to lxml
- Improved regex for emails
- Added different user agents