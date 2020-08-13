# Extract Emails
Extract emails from a given website

## Requirements
- Minimum Python3.6
- requests
- lxml

## Installation
```
pip install extract_emails
```

## Usage
### With default browsers
```
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
```
```
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

```
### With custom browser
```
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
```