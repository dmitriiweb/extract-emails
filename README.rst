Extract Emails
==============

Extract emails from a given website

Requirements
------------

-  Minimum Python3.6
-  requests
-  lxml

Installation
------------

::

    pip install extract_emails

Usage
-----

::

    from extract_emails import ExtractEmails

    em = ExtractEmails(url, depth=None, print_log=False, ssl_verify=True, user_agent=None, request_delay=0.0)
    emails = em.emails

-  *url*: str, ex: http://example.com
-  *depth*: int, depth of scan
-  *print\_log*: boolean, print log or not
-  *ssl\_verify*: boolean
-  *user\_agent*: str
-  *request\_delay*: float

**ssl\_verify** - use to avoid errors like this: \*exceeded with url:
/api/v1/pods?watch=False (Caused by SSLError(SSLError(1, '[SSL:
CERTIFICATE\_VERIFY\_FAILED] certificate verify failed
(\_ssl.c:777)'),))\*

**user\_agent** - you can choose from several user agents: *ie*, *msie*,
*opera*, *chrome*, *google*, *firefox*, *safari*, or *random*

**request_delay** - time delay between requests in seconds

**Return** list of emails.

Changelog
---------
Version 3.0.4
^^^^^^^^^^^^^
- Buf fixing

Version 3.0.3
^^^^^^^^^^^^^
- Improve parser

Version 3.0.1
^^^^^^^^^^^^^
- Minimum Python version: 3.6
- Remove fake_useragent library
- Improve email extraction
- Add time delay between requests

Version 2.0.0
^^^^^^^^^^^^^
-  Replaced BeautifulSoup to lxml
-  Improved regex for emails
-  Added different user agents
