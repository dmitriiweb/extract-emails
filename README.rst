Extract Emails
==============

Extract emails from a given website

Requirements
------------

-  Python3
-  requests
-  beautifulsoup4

Installation
------------

::

    pip install extract_emails

Usage
-----

::

    from extract_emails import ExtractEmails

    em = ExtractEmails(url, depth, print_log)
    emails = em.emails

-  *url*: str, ex: http://example.com
-  *depth*: int, depth of scan
-  *print\_log*: boolean, print log or not

**Return** list of emails.

