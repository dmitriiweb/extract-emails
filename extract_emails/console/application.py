import click


@click.command()
@click.option("--url", type=str, required=True, help="URL to extract data from")
@click.option("-of", "--output-file", type=str, required=True, help="Output CSV file")
@click.option(
    "-b",
    "--browser",
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
def main():
    pass


if __name__ == "__main__":
    main()
