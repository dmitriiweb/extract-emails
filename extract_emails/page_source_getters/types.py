from __future__ import annotations

import typing

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class HtmlPage:
    url: str
    source: str


@dataclass()
class Url:
    url: str
    headers: typing.Optional[dict[str, str] | None] = None
