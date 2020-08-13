# Contributing to extract_emails

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

### Building docs

    make docs

Open `docs/_build/html/index.html` with a browser to see the docs. On macOS you 
can use the following command for that:

    open docs/_build/html/index.html


