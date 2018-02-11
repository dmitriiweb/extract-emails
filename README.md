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

em = ExtractEmails(url, depth=None, print_log=False, ssl_verify=True, user_agent='random')
emails = em.emails
```
- *url*: str, ex: http://example.com
- *depth*: int, depth of scan
- *print_log*: boolean, print log or not
- *ssl_verify*: boolean
- *user_agent*: str

**ssl_verify** - use to avoid errors like this: *exceeded with url: /api/v1/pods?watch=False (Caused by SSLError(SSLError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:777)'),))*

**user_agent** - you can choose from several user agents: *ie*, *msie*, *opera*, *chrome*, *google*, *firefox*, *safari*, or *random*

**Return** list of emails.



## Changelog

#### Version 2.0.0

- Change BeautifulSoup to lxml
- Improved regex for emails
- Added different user agents