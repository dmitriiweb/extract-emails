# Contributing to Extract-Emails

Thanks for taking the time to contribute!

The main goal of the project is extracting different useful information from web pages.
Please feel free to contribute to the project by adding new features, fixing bugs, or share your ideas in the issues section.

## Development environment

The project supports Python 3.10–3.14 and uses `uv` for dependency and
environment management.

```shell
# Install all development and optional-backend dependencies
uv sync --all-extras

# Activate the environment if desired
source .venv/bin/activate
```

## Tests

Write tests with [pytest](https://docs.pytest.org/). The default test command
excludes slow and browser-dependent checks; it uses deterministic local
fixtures, not external websites.

```shell
# Offline/default suite
make test

# All tests, including browser tests
make test-all

# Explicit browser test suite
make test-browsers
```

The browser suite uses local HTTP fixtures and requires Chromium. Install it
for the Playwright environment with:

```shell
uv run playwright install chromium --with-deps
```

Browser coverage is an explicit local smoke suite; network-dependent external
site checks are not release gates.

## Formatting and linting

Ruff is the shared formatter, import sorter, and linter in Make and pre-commit.
Use the repository targets so local checks match the configured hooks:

```shell
make format
make lint
```

`make lint` also runs mypy.

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
