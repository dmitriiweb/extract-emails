from pathlib import Path

import click

from extract_emails import browsers
from extract_emails.data_extractors import (
    DataExtractor,
    EmailExtractor,
    LinkedinExtractor,
)
from extract_emails.models.page_data import PageData
from extract_emails.workers import DefaultWorker


def get_data_extractors(data_type: str) -> list[DataExtractor]:
    if data_type == "email":
        return [EmailExtractor()]
    elif data_type == "linkedin":
        return [LinkedinExtractor()]
    else:
        raise ValueError(f"Invalid data type: {data_type}")


def get_browser(browser: str) -> browsers.PageSourceGetter:
    if browser == "httpx":
        return browsers.HttpxBrowser()
    elif browser == "chromium":
        return browsers.ChromiumBrowser()
    else:
        raise ValueError(f"Invalid browser: {browser}")


@click.command()
@click.option("--url", type=str, required=True, help="URL to extract data from")
@click.option("-of", "--output-file", type=str, required=True, help="Output CSV file")
@click.option(
    "-b",
    "--browser-name",
    type=str,
    default="chromium",
    help="Browser to use, can be 'chromium' or 'httpx'. Default: chromium",
)
@click.option(
    "-dt",
    "--data-type",
    type=str,
    default="email",
    help="Data type to extract, must be a list separated by comma, e.g. 'email,linkedin. "
    "Available options: email, linkedin. Default: email,linkedin",
)
def main(url: str, output_file: str, browser_name: str, data_type: str):
    browser = get_browser(browser_name)
    browser.start()

    worker = DefaultWorker(
        website_url=url,
        browser=browser,
        data_extractors=get_data_extractors(data_type),
    )
    data = worker.get_data()

    browser.stop()

    PageData.save_as_csv(data, Path(output_file))


if __name__ == "__main__":
    main()
