from typing import Optional

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from .browser_interface import BrowserInterface


class ChromeBrowser(BrowserInterface):
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

    def __init__(self,
                 headless: Optional[bool] = True,
                 executable_path: Optional[str] = 'chromedriver'):
        self.executable_path = executable_path
        self._chrome_options = Options()
        self._chrome_options.add_argument('--disable-gpu')
        self._chrome_options.add_argument('--disable-software-rasterizer')
        if headless:
            self._chrome_options.add_argument('--headless')
        self._chrome_options.add_argument('--disable-dev-shm-usage')
        self._chrome_options.add_argument("--window-size=1920x1080")
        self._chrome_options.add_argument('--disable-setuid-sandbox')
        self._chrome_options.add_argument('--no-sandbox')
        self._driver = None

    def open(self):
        self._driver = webdriver.Chrome(options=self._chrome_options, executable_path=self.executable_path)

    def close(self):
        self._driver.close()
        self._driver.quit()

    def _get(self, url: str) -> bool:
        try:
            self._driver.get(url)
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
        is_get = self._get(url)
        if is_get:
            return self._driver.page_source
        return ''
