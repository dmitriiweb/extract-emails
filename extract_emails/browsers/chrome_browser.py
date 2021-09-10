from os import PathLike
from typing import Iterable
from typing import Optional

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from extract_emails.browsers import PageSourceGetter

from .browser_interface import BrowserInterface


"""
Chrome Browser
---------------
Make GET requests via selenium + Google Chrome Browser

:param bool headless: run browser in headless mode, default: True
:param str executable_path: path to the executable. If the default is used it assumes the executable is in the $PATH

**Example:**
::

    browser = ChromeBrowser()
    browser.open()
    page_source = browser.get_page_source('https://example.com')
    browser.close()
"""


class ChromeBrowser(PageSourceGetter):
    default_options = {
        "--disable-gpu",
        "--disable-software-rasterizer",
        "--disable-dev-shm-usage",
        "--window-size=1920x1080",
        "--disable-setuid-sandbox",
        "--no-sandbox",
    }

    def __init__(
        self,
        executable_path: PathLike = "/usr/bin/chromedriver",
        headless_mode: bool = True,
        options: Iterable[str] = None,
    ):
        self.executable_path = executable_path
        self.headless_mode = headless_mode
        self.options = options if options is not None else self.default_options
        self.driver = None

    def open(self):
        """Add arguments to chrome.Options() and run the browser"""
        options = Options()
        for option in self.options:
            options.add_argument(option)

        if self.headless_mode:
            options.add_argument("--headless")

        self.driver = webdriver.Chrome(
            options=options, executable_path=self.executable_path
        )

    def close(self):
        self.driver.close()
        self.driver.quit()

    def _get(self, url: str) -> bool:
        try:
            self.driver.get(url)
            return True
        except:
            return False

    def get_page_source(self, url: str) -> str:
        """
        Return page source from url

        :param str url: page url
        :return: str, HTML from page

        **Example:**
        ::

            page_source = browser.get_page_source('https://example.com')
        """
        is_get = self.get(url)
        if is_get:
            return self.driver.page_source
        return ""
