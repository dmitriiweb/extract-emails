version := $(shell python -c 'from extract_emails import __version__; print(__version__)')

.PHONY: test
test:
	pytest --cov=extract_emails -vv -m "not slow" tests/

.PHONY: test-all
test-all:
	pytest --cov=extract_emails -vv tests/

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
