from importlib import import_module
from typing import TYPE_CHECKING

from .page_source_getter import PageSourceGetter

__all__ = ("PageSourceGetter", "ChromiumBrowser", "HttpxBrowser")

if TYPE_CHECKING:
    from .chromium_browser import ChromiumBrowser
    from .httpx_browser import HttpxBrowser


def __getattr__(name: str):
    if name == "ChromiumBrowser":
        module_name, class_name, dependency, extra = (
            ".chromium_browser",
            "ChromiumBrowser",
            "playwright",
            "playwright",
        )
    elif name == "HttpxBrowser":
        module_name, class_name, dependency, extra = (
            ".httpx_browser",
            "HttpxBrowser",
            "httpx",
            "httpx",
        )
    else:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    try:
        browser_class = getattr(import_module(module_name, __name__), class_name)
    except ModuleNotFoundError as error:
        if error.name != dependency:
            raise
        raise ImportError(
            f"{name} requires the optional dependency; install extract-emails[{extra}]"
        ) from error
    globals()[name] = browser_class
    return browser_class
