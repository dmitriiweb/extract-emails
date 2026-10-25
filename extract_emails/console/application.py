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


def _parse_data_types(data_type: str) -> list[str]:
    """Parse comma-separated data type names, preserving their first occurrence.

    Args:
        data_type: Comma-separated data type names.

    Returns:
        Unique data type names in input order.

    Raises:
        click.BadParameter: If a token is empty or unsupported.
    """
    supported = {"email", "linkedin"}
    parsed: list[str] = []
    seen: set[str] = set()
    for token in data_type.split(","):
        normalized = token.strip()
        if not normalized or normalized not in supported:
            raise click.BadParameter(
                f"Invalid data type: {normalized or '<empty>'}",
                param_hint="--data-type",
            )
        if normalized not in seen:
            parsed.append(normalized)
            seen.add(normalized)
    return parsed


def get_data_extractors(data_type: str) -> list[DataExtractor]:
    """Create extractors for comma-separated data types.

    Args:
        data_type: Comma-separated data type names.

    Returns:
        Extractors in the order of their first corresponding type.

    Raises:
        click.BadParameter: If a token is empty or unsupported.
    """
    extractor_types: dict[str, type[DataExtractor]] = {
        "email": EmailExtractor,
        "linkedin": LinkedinExtractor,
    }
    return [extractor_types[name]() for name in _parse_data_types(data_type)]


def _validate_data_type(ctx: click.Context, param: click.Parameter, value: str) -> str:
    """Validate and normalize the data-type option before command execution.

    Args:
        ctx: Click command context.
        param: The option being validated.
        value: Raw comma-separated option value.

    Returns:
        Comma-separated unique data type names in input order.
    """
    del ctx, param
    return ",".join(_parse_data_types(value))


def get_browser(browser: str) -> browsers.PageSourceGetter:
    """Create the selected browser backend.

    Args:
        browser: Browser backend name.

    Returns:
        The selected page source getter.

    Raises:
        ValueError: If the browser name is unsupported.
    """
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
    type=click.Choice(["chromium", "httpx"]),
    default="chromium",
    show_default=True,
    help="Browser to use.",
)
@click.option(
    "-dt",
    "--data-type",
    type=str,
    default="email",
    show_default=True,
    callback=_validate_data_type,
    help="Comma-separated data types to extract: email, linkedin.",
)
def main(url: str, output_file: str, browser_name: str, data_type: str) -> None:
    """Extract requested data from a website and save it as CSV.

    Args:
        url: URL to extract data from.
        output_file: Destination CSV path.
        browser_name: Browser backend to use.
        data_type: Comma-separated data types to extract.
    """
    extractors = get_data_extractors(data_type)
    with get_browser(browser_name) as browser:
        worker = DefaultWorker(
            website_url=url,
            browser=browser,
            data_extractors=extractors,
        )
        data = worker.get_data()

    PageData.to_csv(data, Path(output_file))


if __name__ == "__main__":
    main()
