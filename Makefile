version := $(shell uv run python -c 'from extract_emails import __version__; print(__version__)')

.PHONY: test
test:
	uv run pytest --cov=extract_emails -vv -m "not slow" tests/

.PHONY: test-all
test-all:
	uv run pytest --cov=extract_emails -vv tests/

.PHONY: format
format:
	uv run ruff check extract_emails tests --select I --fix
	uv run ruff format extract_emails tests

.PHONY: lint
lint:
	uv run ruff check extract_emails
	uv run mypy extract_emails

.PHONY: docs-serve
docs-serve:
	uv run mkdocs serve

.PHONY: docs-publish
docs-publish:
	uv run mkdocs gh-deploy --force

.PHONY: publish
publish:
	uv build
	uv publish
