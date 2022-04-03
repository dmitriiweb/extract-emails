from pathlib import Path
from typing import List
from typing import Type
from typing import Union

import click

from extract_emails import ContactFilterAndEmailAndLinkedinFactory
from extract_emails import ContactFilterAndEmailFactory
from extract_emails import ContactFilterAndLinkedinFactory
from extract_emails import DefaultWorker
from extract_emails.browsers.chrome_browser import ChromeBrowser
from extract_emails.browsers.requests_browser import RequestsBrowser
from extract_emails.data_savers import CsvSaver
from extract_emails.factories.base_factory import BaseFactory


def get_factory(data_type: List[str]) -> Type[BaseFactory]:
    if data_type == ["email"]:
        return ContactFilterAndEmailFactory
    elif data_type == ["linkedin"]:
        return ContactFilterAndLinkedinFactory
    elif "email" in data_type and "linkedin" in data_type:
        return ContactFilterAndEmailAndLinkedinFactory
    else:
        raise ValueError(f"Invalid data type: {data_type}")


def get_browser(browser: str) -> Union[ChromeBrowser, RequestsBrowser]:
    if browser == "requests":
        return RequestsBrowser()
    elif browser == "chrome":
        b = ChromeBrowser()
        b.open()
        return b
    else:
        raise ValueError(f"Invalid browser: {browser}")


@click.command()
@click.option("--url", type=str, required=True, help="URL to extract data from")
@click.option("-of", "--output-file", type=str, required=True, help="Output CSV file")
@click.option(
    "-b",
    "--browser-name",
    type=str,
    default="chrome",
    help="Browser to use, can be 'chrome' or 'requests'. Default: chrome",
)
@click.option(
    "-dt",
    "--data-type",
    type=str,
    default="email",
    help="Data type to extract, must be a list separated by comma, e.g. 'email,linkedin. "
    "Available options: email, linkedin. Default: email",
)
@click.option(
    "-d", "--depth", type=int, default=10, help="Depth of the search. Default: 10"
)
def main(url: str, output_file: str, browser_name: str, data_type: str, depth: int):
    tfactory = get_factory(data_type=[i.strip() for i in data_type.split(",")])
    browser = get_browser(browser_name)

    factory = tfactory(website_url=url, browser=browser, depth=depth)

    worker = DefaultWorker(factory=factory)
    data = worker.get_data()

    if browser_name == "chrome":
        browser.close()

    saver = CsvSaver(output_path=Path(output_file))
    saver.save(data)


if __name__ == "__main__":
    main()
