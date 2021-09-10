version := $(shell python -c 'from extract_emails import __version__; print(__version__)')

.PHONY: test
test:
	pytest --cov=extract_emails -vv -m "not slow" tests/

.PHONY: test-all
test-all:
	pytest --cov=extract_emails -vv tests/
