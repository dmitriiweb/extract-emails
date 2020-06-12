.. extract_emails documentation master file, created by
   sphinx-quickstart on Sat May  2 14:47:14 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   index

Installation
~~~~~~~~~~~~
::

   pip install extract_emails

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
~~~~~~~~~
Interface
---------
.. autoclass:: extract_emails.email_filters.EmailFilterInterface
   :members:

DefaultEmailFilter
---------
.. autoclass:: extract_emails.email_filters.DefaultEmailFilter
   :members:

Links Filters
~~~~~~~~~
Interface
---------
.. autoclass:: extract_emails.link_filters.LinkFilterInterface
   :members:

DefaultLinkFilter
---------
.. autoclass:: extract_emails.link_filters.DefaultLinkFilter
   :members:
