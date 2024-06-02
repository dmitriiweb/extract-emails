# Changelog

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
