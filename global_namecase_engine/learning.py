"""Heuristic helpers for discovering candidate particles."""

from __future__ import annotations

from collections import Counter
from typing import Iterable, List, Optional, Set

from .config import DEFAULT_PARTICLE_PHRASES
from .tokenizer import tokenize


def discover_particles(
    names: Iterable[str],
    *,
    min_count: int = 3,
    max_token_length: int = 4,
    known_particles: Optional[Iterable[str]] = None,
) -> List[str]:
    """Return frequent interior tokens that may be worth reviewing as particles."""

    if min_count < 1:
        raise ValueError("min_count must be at least 1")

    known: Set[str] = set(known_particles or ())
    known.update(token for phrase in DEFAULT_PARTICLE_PHRASES for token in phrase)

    counter: Counter[str] = Counter()
    for name in names:
        tokens = [token.lower() for token in tokenize(name) if token]
        if len(tokens) < 3:
            continue
        for token in tokens[1:-1]:
            if not token.isalpha():
                continue
            if len(token) > max_token_length:
                continue
            if token in known:
                continue
            counter[token] += 1

    return [
        token
        for token, count in counter.most_common()
        if count >= min_count
    ]
