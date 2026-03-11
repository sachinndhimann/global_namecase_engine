"""Whitespace and punctuation normalization helpers."""

from __future__ import annotations

import re
from typing import List

UNICODE_APOSTROPHES = {"\u2018", "\u2019", "\u02bc", "\u2032"}
UNICODE_DASHES = {"\u2010", "\u2011", "\u2012", "\u2013", "\u2014", "\u2212"}

_WHITESPACE_RE = re.compile(r"\s+")


def normalize_separators(value: str) -> str:
    """Collapse whitespace and normalize common apostrophe and dash variants."""

    normalized = value.strip()
    for apostrophe in UNICODE_APOSTROPHES:
        normalized = normalized.replace(apostrophe, "'")
    for dash in UNICODE_DASHES:
        normalized = normalized.replace(dash, "-")
    return _WHITESPACE_RE.sub(" ", normalized)


def tokenize(value: str) -> List[str]:
    """Tokenize a normalized name on spaces."""

    normalized = normalize_separators(value)
    if not normalized:
        return []
    return normalized.split(" ")
