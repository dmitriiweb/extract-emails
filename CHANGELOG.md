# Changelog

## 6.0.2

### Added
- GitHub Actions workflows for automated testing and publishing
- `AGENTS.md` documentation file with repository structure and workflow rules
- Codex skills structure (`.codex/skills/`) with multiple assistant skills:
  - agents-md-assistant
  - code-review-assistant
  - debug-logging-assistant
  - format-lint-assistant
  - git-commit-assistant
  - google-docstring-assistant
  - pytest-testing-assistant
  - skill-creator
  - uv-package-management-assistant

### Changed
- Migrated from `.cursor/rules/` to `.codex/skills/` structure
- Pinned `pydantic` to version 2.12.0
- Updated `tox.ini` configuration
- Added Python 3.14 support to classifiers

### Removed
- Removed `.cursor/rules/` files (migrated to `.codex/skills/` structure)
- Removed `.cursor/commands/git-commit.md` (moved to skills structure)

## 6.0.1

### Added
- Added `pytest-asyncio` dependency for async test support

### Changed
- `HttpxBrowser` now sets a default User-Agent header when none is provided (fixes Wikipedia and other sites that block requests without user-agent)
- Converted `ChromiumBrowser` tests to use async methods for compatibility with pytest asyncio mode
- Updated `pytest.ini` to include `asyncio_mode = auto` for automatic async test detection
- Fixed test method name: `PageData.save_as_csv` → `PageData.to_csv` in test suite

### Fixed
- Fixed async/sync API conflict in ChromiumBrowser tests when running in pytest asyncio mode
- Fixed test failures due to missing user-agent header in HttpxBrowser

## 6.0.0

### Added
- New browser backends: `ChromiumBrowser` (sync/async, via Playwright) and `HttpxBrowser` (sync/async, via httpx)
- Async CSV saving: `PageData.ato_csv` for async CSV export
- Full async/sync support for all main workflows

### Changed
- Refactored `PageData.save_as_csv` → `PageData.to_csv` (sync) and added `ato_csv` (async)
- Refactored and improved `DefaultWorker` (sync/async extraction, more robust)
- Updated documentation and quick start guides for new API and CLI
- Updated test suite for new browser backends

### Removed
- Removed all old factory classes and related docs
- Removed legacy browsers: `chrome_browser.py`, `requests_browser.py`
- Removed all old factory-based test and code paths

### Other
- Switched package/dependency management from Poetry to `uv`
- Updated Python support: now requires Python 3.10+
- Updated dependencies

## 5.3.4

### Changed

- Drop python 3.9 support
- Update dependencies
- Update readme

## 5.3.2

### Changed

- Update dependencies and supported python versions
- minor fixes and code formatting

## 5.3.1

### Changed

- Add timeout to RequestBrowser

    ```python
    from extract_emails.browsers.requests_browser import RequestsBrowser as Browser
  
    browser = Browser()
    browser.requests_timeout = 1
    ```

## 5.3.0

### Changed

- Add custom save mode to csv data saver

## 5.2.0

### Added

- CLI tool
- csv data saver

## 5.1.3

### Changed

- Update dependencies

## 5.1.2

### Added

- Python 3.10 support
- Add CHANGELOG.md

## 5.1.0

### Added

- Add save_as_csv class method to `PageData` model
- Add logs to DefaultWorker

### Changed

- Check if needed libraries for browsers were installed. If not will show user-friendly error
- Small improvements in the code

## 5.0.2

### Changed

- Fix imports for factories and DefaultWorker
