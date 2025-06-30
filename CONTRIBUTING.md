# Contributing to Extract-Emails

Thanks for taking the time to contribute!

The main goal of the project is extracting different useful information from web pages.
Please feel free to contribute to the project by adding new features, fixing bugs, or share your ideas in the issues section.

## Virtual environment
You can create a virtual environment using [poetry](https://python-poetry.org/docs/):
```shell
# Install dependencies
uv sync --all-extras

# Activate the virtual environment
source .venv/bin/activate
```

## Tests
All testes must be written with [pytest](https://docs.pytest.org/) library.

To run tests, run the following commands:
```shell
# run all tests
make test-all

# run tests without slow cases
make test
```

## Documentation
For rendering documentation use [mkdocs](https://mkdocs.org/), so all docstrings must be
written in [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)

```shell
# Serve docs
make docs-serve
```

## Commits
Please use the following template for commits:
```shell
type: title

body[optional]
```
for example:
```shell
feat: add new feature
```

The commit type is one of the following:

- *feat* - a new feature
- *fix* - a bug fix
- *chore* - changes to the project's internals (e.g. dependency updates)
- *refactor* - a change that neither fixes a bug nor adds a feature
- *docs* - documentation only changes
- *test* - changes to the test suite
- etc
