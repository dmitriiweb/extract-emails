.. extract_emails documentation master file, created by
   sphinx-quickstart on Sat May  2 14:47:14 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   index

Installation
~~~~~~~~~~~~~
::

   pip install extract_emails

Usage
~~~~~~
With default browsers
---------------------------
::
   
   from extract_emails import EmailExtractor
   from extract_emails.browsers import ChromeBrowser


   with ChromeBrowser() as browser:
       email_extractor = EmailExtractor("http://www.tomatinos.com/", browser, depth=2)
       emails = email_extractor.get_emails()


   for email in emails:
       print(email)
       print(email.as_dict())

   # Email(email="bakedincloverdale@gmail.com", source_page="http://www.tomatinos.com/")
   # {'email': 'bakedincloverdale@gmail.com', 'source_page': 'http://www.tomatinos.com/'}
   # Email(email="freshlybakedincloverdale@gmail.com", source_page="http://www.tomatinos.com/")
   # {'email': 'freshlybakedincloverdale@gmail.com', 'source_page': 'http://www.tomatinos.com/'}


::

   from extract_emails import EmailExtractor
   from extract_emails.browsers import RequestsBrowser


   with RequestsBrowser() as browser:
       email_extractor = EmailExtractor("http://www.tomatinos.com/", browser, depth=2)
       emails = email_extractor.get_emails()


   for email in emails:
       print(email)
       print(email.as_dict())

   # Email(email="bakedincloverdale@gmail.com", source_page="http://www.tomatinos.com/")
   # {'email': 'bakedincloverdale@gmail.com', 'source_page': 'http://www.tomatinos.com/'}
   # Email(email="freshlybakedincloverdale@gmail.com", source_page="http://www.tomatinos.com/")
   # {'email': 'freshlybakedincloverdale@gmail.com', 'source_page': 'http://www.tomatinos.com/'}

With custom browser
-------------------
::

   from extract_emails import EmailExtractor
   from extract_emails.browsers import BrowserInterface
   
   from selenium import webdriver
   from selenium.webdriver.firefox.options import Options
   
   
   class FirefoxBrowser(BrowserInterface):
       def __init__(self):
           ff_options = Options()
           self._driver = webdriver.Firefox(
               options=ff_options, executable_path="/home/di/geckodriver",
           )
   
       def close(self):
           self._driver.quit()
   
       def get_page_source(self, url: str) -> str:
           self._driver.get(url)
           return self._driver.page_source
   
   
   with FirefoxBrowser() as browser:
       email_extractor = EmailExtractor("http://www.tomatinos.com/", browser, depth=2)
       emails = email_extractor.get_emails()
   
   for email in emails:
       print(email)
       print(email.as_dict())
   
   # Email(email="bakedincloverdale@gmail.com", source_page="http://www.tomatinos.com/")
   # {'email': 'bakedincloverdale@gmail.com', 'source_page': 'http://www.tomatinos.com/'}
   # Email(email="freshlybakedincloverdale@gmail.com", source_page="http://www.tomatinos.com/")
   # {'email': 'freshlybakedincloverdale@gmail.com', 'source_page': 'http://www.tomatinos.com/'}

EmailExtractor
~~~~~~~~~~~~~~~
.. autoclass:: extract_emails.EmailExtractor
   :members:

Email
~~~~~
.. autoclass:: extract_emails.email.Email
   :members:

Browsers
~~~~~~~~~
Interface
---------
.. autoclass:: extract_emails.browsers.BrowserInterface
   :members:

RequestsBrowser
---------------
.. autoclass:: extract_emails.browsers.RequestsBrowser
   :members:

ChromeBrowser
---------------
.. autoclass:: extract_emails.browsers.ChromeBrowser
   :members:

HTML Handlers
~~~~~~~~~~~~~~
Interface
---------
.. autoclass:: extract_emails.html_handlers.HTMLHandlerInterface
   :members:

DefaultHTMLHandler
--------------------
.. autoclass:: extract_emails.html_handlers.DefaultHTMLHandler
   :members:

Emails Filters
~~~~~~~~~~~~~~
Interface
----------
.. autoclass:: extract_emails.email_filters.EmailFilterInterface
   :members:

DefaultEmailFilter
------------------
.. autoclass:: extract_emails.email_filters.DefaultEmailFilter
   :members:

Links Filters
~~~~~~~~~~~~~~
Interface
---------
.. autoclass:: extract_emails.link_filters.LinkFilterInterface
   :members:

DefaultLinkFilter
------------------
.. autoclass:: extract_emails.link_filters.DefaultLinkFilter
   :members:

ContactInfoLinkFilter
------------------
.. autoclass:: extract_emails.link_filters.ContactInfoLinkFilter
   :members:

