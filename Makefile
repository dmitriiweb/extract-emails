version := $(shell python -c 'from extract_emails import __version__; print(__version__)')

.PHONY: test
test:
	pytest --cov=extract_emails -vv -m "not slow" tests/

.PHONY: test-all
test-all:
	pytest --cov=extract_emails -vv tests/

.PHONY: code-format
code-format:
	isort extract_emails tests
	ruff format extract_emails tests

.PHONY: code-check
code-check:
	ruff extract_emails tests
	mypy extract_emails

.PHONY: docs-serve
docs-serve:
	mkdocs serve

.PHONY: docs-publish
docs-publish:
	mkdocs gh-deploy --force

.PHONY: publish
publish:
	poetry build
	poetry publish
