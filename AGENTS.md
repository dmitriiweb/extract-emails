# AGENTS.md — Agent instructions for this repository

## Goals
- Primary goal: Extract email addresses and LinkedIn profiles from websites with correct behavior and passing tests
- Secondary goals: Maintain clean architecture with pluggable browsers, extractors, and filters; keep public APIs stable

## Setup & daily commands (run these)
- Install deps: `uv sync --all-extras`
- Start dev: N/A (library, not a service)
- Lint: `make lint` (runs `ruff check` and `mypy`)
- Format: `make format` (runs `ruff check --select I --fix` and `ruff format`)
- Typecheck: `make lint` (includes mypy)
- Test (all): `make test-all` (runs all tests including slow ones)
- Test (single): `make test` (excludes slow tests) or `uv run pytest tests/test_email_extractor.py::test_specific_test`
- Build: `uv build`
- Publish: `make publish` (builds and publishes to PyPI)
- Docs serve: `make docs-serve` (runs `mkdocs serve`)
- Docs publish: `make docs-publish` (deploys to GitHub Pages)

## Repo map (where to look / write)
- `extract_emails/` — main package source code
  - `browsers/` — browser implementations (ChromiumBrowser, HttpxBrowser)
  - `data_extractors/` — extractors for emails and LinkedIn profiles
  - `data_savers/` — data saving implementations (CSV)
  - `link_filters/` — link filtering logic (ContactInfoLinkFilter, DefaultLinkFilter)
  - `models/` — data models (PageData)
  - `utils/` — utility functions (email filtering, TLD validation)
  - `workers/` — main worker orchestration (DefaultWorker)
  - `console/` — CLI application entry point
- `tests/` — pytest test suite (mirrors source structure)
- `docs/` — mkdocs documentation
- `mkdocs.yml` — documentation configuration
- Generated / do-not-edit: `.venv/`, `dist/`, `build/`, `*.egg-info/`, `site/` (docs build output)

## Architecture snapshot
- **Data flow**: `DefaultWorker` → `Browser` (PageSourceGetter) → `LinkFilter` → `DataExtractor` → `PageData`
- **Key entrypoints**: 
  - Library: `extract_emails.DefaultWorker`
  - CLI: `extract_emails.console.application:main` (via `extract-emails` command)
- **Key configs**: `pyproject.toml`, `pytest.ini`, `mkdocs.yml`, `Makefile`
- **Components**:
  - **Workers**: Orchestrate extraction with depth-limited crawling
  - **Browsers**: Abstract page source fetching (ChromiumBrowser for JS-rendered pages, HttpxBrowser for static)
  - **Link Filters**: Determine which links to follow (ContactInfoLinkFilter focuses on contact/about pages)
  - **Data Extractors**: Extract specific data types (EmailExtractor, LinkedinExtractor)
  - **Models**: PageData aggregates extracted data per page

## Dev environment
- Required versions: Python >=3.10,<3.15, uv (package manager)
- Required services: None (standalone library)
- Optional dependencies:
  - `playwright` for ChromiumBrowser (requires `playwright install chromium --with-deps`)
  - `httpx` for HttpxBrowser
- Env vars: None required
- Migrations/seed: N/A

## Workflow rules
- Branching: Feature branches from main (conventional commits)
- PR expectations: 
  - All tests must pass (`make test-all`)
  - Lint and typecheck must pass (`make lint`)
  - Update docs when behavior changes
  - Use Google-style docstrings for new code
- Commit format: `type: title` (e.g., `feat: add new feature`, `fix: bug fix`, `docs: update README`)
- Release/versioning: Semantic versioning, version in `extract_emails/__init__.py` and `pyproject.toml`

## Code style & patterns
- Formatting: `ruff format` (with `ruff check --select I --fix` for imports)
- Type checking: `mypy` (strict mode)
- Conventions: 
  - Snake_case for modules and functions
  - Clear separation: browsers, extractors, filters, workers
  - Abstract base classes for extensibility (PageSourceGetter, DataExtractor, LinkFilterBase)
  - Support both sync and async APIs
- Error handling: 
  - Log errors via `loguru` logger
  - Continue processing on individual page failures
  - Raise exceptions for configuration errors
- Documentation: Google-style docstrings (required for mkdocs)
- Example (good):
  ```python
  from extract_emails import DefaultWorker
  from extract_emails.browsers import ChromiumBrowser
  from extract_emails.models import PageData

  with ChromiumBrowser() as browser:
      worker = DefaultWorker("https://example.com", browser)
      data = worker.get_data()
      PageData.to_csv(data, Path("output.csv"))
  ```
