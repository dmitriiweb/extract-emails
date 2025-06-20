version := $(shell python -c 'from extract_emails import __version__; print(__version__)')

.PHONY: test
test:
	pytest --cov=extract_emails -vv -m "not slow" tests/

.PHONY: test-all
test-all:
	pytest --cov=extract_emails -vv tests/

.PHONY: format
format:
	ruff check extract_emails tests --select I --fix
	ruff format extract_emails tests

.PHONY: code-check
code-check:
	ruff check extract_emails
	mypy extract_emails

.PHONY: docs-serve
docs-serve:
	mkdocs serve

.PHONY: docs-publish
docs-publish:
	mkdocs gh-deploy --force

.PHONY: publish
publish:
	uv build
	uv publish
