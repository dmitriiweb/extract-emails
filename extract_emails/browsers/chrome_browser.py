import time

from os import PathLike
from typing import Iterable
from typing import Optional

from loguru import logger

from extract_emails.errors import BrowserImportError


try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
except ModuleNotFoundError:
    msg = "ChromeBrowser require selenium library:\n\n\tpip install selenium\n\tpoetry add selenium\n"
    raise BrowserImportError(msg)

from extract_emails.browsers.page_source_getter import PageSourceGetter


class ChromeBrowser(PageSourceGetter):
    """Getting page sources with selenium and chromedriver

    Examples:
        >>> from extract_emails.browsers.chrome_browser import ChromeBrowser
        >>> browser = ChromeBrowser()
        >>> browser.open()
        >>> page_source = browser.get_page_source('https://example.com')
        >>> browser.close()

        >>> from extract_emails.browsers.chrome_browser import ChromeBrowser
        >>> with ChromeBrowser() as browser:
        ...     page_source = browser.get_page_source('https://example.com')

    """

    default_options = {
        "--disable-gpu",
        "--disable-software-rasterizer",
        "--disable-dev-shm-usage",
        "--window-size=1920x1080",
        "--disable-setuid-sandbox",
        "--no-sandbox",
    }
    wait_seconds_after_get = 0

    def __init__(
        self,
        executable_path: PathLike = "/usr/bin/chromedriver",
        headless_mode: bool = True,
        options: Iterable[str] = None,
    ) -> None:
        """ChromeBrowser initialization

        Args:
            executable_path: path to chromedriver, use `which chromedriver` to get the path.
                Default: /usr/bin/chromedriver
            headless_mode: run browser with headless mode or not. Default: True
            options: arguments for chrome.Options().
                Default: set("--disable-gpu", "--disable-software-rasterizer", "--disable-dev-shm-usage",
                    "--window-size=1920x1080", "--disable-setuid-sandbox", "--no-sandbox", )
        """
        self.executable_path = executable_path
        self.headless_mode = headless_mode
        self.options = options if options is not None else self.default_options
        self.driver: Optional[webdriver.Chrome] = None

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

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
        """Close the browser"""
        self.driver.close()
        self.driver.quit()

    def get_page_source(self, url: str) -> str:
        """Get page source text from URL

        Args:
            url: URL

        Returns:
            page source as text
        """
        try:
            self.driver.get(url)
            time.sleep(self.wait_seconds_after_get)
            page_source = self.driver.page_source
        except Exception as e:
            logger.error(f"Could not get page source from {url}: {e}")
            return ""

        if "<html><head></head><body></body></html>" == page_source:
            logger.error(f"Could not get page source from {url}: Unknown reason")

        return page_source
