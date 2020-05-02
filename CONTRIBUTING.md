# Contributing to extract_emails

## Submitting patches

If you contribute code to extract_emails, you agree to license your code under the MIT.

The new code should follow [PEP8](https://pep8.org/) coding style (except
the line length limit, which is 90) and adhere to the style of 
the surrounding code.

You must document any functionality using Sphinx-compatible RST, and
implement tests for any functionality in the `test` directory.

In your Pull Requests there's no need to fill the changelog or AUTHORS,
this is a maintainer's responsibility.

If your PR remains unreviewed for a while, feel free to bug the maintainer.


### Setup

1.  Create a virtualenv
2.  Install `extract_emails` in editable mode along with dev dependencies:

        pip install -e ".[dev]"

3.  Ensure that tests pass

        make test


### Running tests

To run the full test suite:

    make test

Or simply:

    pytest

Before pushing your code, make sure that linting passes, otherwise Travis
build would fail:

    make lint


### Building docs

    make docs

Open `docs/_build/html/index.html` with a browser to see the docs. On macOS you 
can use the following command for that:

    open docs/_build/html/index.html


