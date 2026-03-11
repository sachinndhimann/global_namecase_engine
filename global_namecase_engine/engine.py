"""Core engine for deterministic human-name casing."""

from __future__ import annotations

from dataclasses import dataclass
import re
from typing import List, Optional, Sequence

from .config import NameCaseConfig
from .tokenizer import tokenize


@dataclass(frozen=True, slots=True)
class _TokenParts:
    leading: str
    core: str
    trailing: str


def _split_outer_punctuation(token: str) -> _TokenParts:
    start = 0
    end = len(token)

    while start < end and not token[start].isalnum():
        start += 1

    while end > start and not token[end - 1].isalnum() and token[end - 1] != ".":
        end -= 1

    return _TokenParts(
        leading=token[:start],
        core=token[start:end],
        trailing=token[end:],
    )


def _simple_title(token: str) -> str:
    return token[:1].upper() + token[1:].lower() if token else token


class NameCaseEngine:
    """Deterministic name normalizer with conservative heuristics."""

    def __init__(self, config: Optional[NameCaseConfig] = None) -> None:
        self.config = config or NameCaseConfig()
        self._particle_phrases = sorted(
            self.config.particle_phrases,
            key=len,
            reverse=True,
        )

    def normalize(self, name: Optional[str]) -> Optional[str]:
        """Normalize a name string while preserving deterministic output."""

        if name is None:
            return None
        if not isinstance(name, str):
            raise TypeError("name must be a string or None")

        tokens = tokenize(name)
        if not tokens:
            return ""

        normalized = [self._normalize_token(token) for token in tokens]
        lowered = [self._match_key(token) for token in tokens]
        self._apply_particle_phrases(normalized, lowered)
        self._apply_suffixes(normalized, lowered)
        return " ".join(normalized)

    def _normalize_token(self, token: str) -> str:
        parts = _split_outer_punctuation(token)
        if not parts.core:
            return token

        normalized_core = self._normalize_core(parts.core)
        return f"{parts.leading}{normalized_core}{parts.trailing}"

    def _normalize_core(self, token: str) -> str:
        match_key = token.lower()
        exception = self.config.exceptions.get(match_key)
        if exception is not None:
            return exception

        if self._is_initial(match_key):
            letters = [character.upper() for character in token if character.isalpha()]
            return ".".join(letters) + "."

        if "-" in token:
            return "-".join(self._normalize_core(part) for part in token.split("-"))

        if "'" in token:
            return self._normalize_apostrophe_token(token)

        if match_key.startswith("mc") and len(match_key) > 2 and match_key[2].isalpha():
            return "Mc" + _simple_title(match_key[2:])

        return _simple_title(token)

    def _normalize_apostrophe_token(self, token: str) -> str:
        parts = token.split("'")
        if len(parts) == 1:
            return _simple_title(token)

        normalized_parts: List[str] = []
        for index, part in enumerate(parts):
            lower_part = part.lower()
            if not part:
                normalized_parts.append(part)
            elif index == 0 and lower_part in self.config.lowercase_apostrophe_prefixes:
                normalized_parts.append(lower_part)
            elif index == 0 and lower_part in self.config.titlecase_apostrophe_prefixes:
                normalized_parts.append(_simple_title(part))
            else:
                normalized_parts.append(self._normalize_core(part))

        return "'".join(normalized_parts)

    def _apply_particle_phrases(
        self,
        normalized_tokens: List[str],
        lowered_tokens: Sequence[str],
    ) -> None:
        for index in range(len(lowered_tokens)):
            for phrase in self._particle_phrases:
                phrase_length = len(phrase)
                if tuple(lowered_tokens[index : index + phrase_length]) != phrase:
                    continue
                if index == 0 and not self.config.lowercase_leading_particles:
                    continue
                for offset in range(phrase_length):
                    normalized_tokens[index + offset] = normalized_tokens[index + offset].lower()
                break

    def _apply_suffixes(
        self,
        normalized_tokens: List[str],
        lowered_tokens: Sequence[str],
    ) -> None:
        for index, token in enumerate(lowered_tokens):
            if index == 0:
                continue
            canonical = self.config.suffixes.get(token)
            if canonical is not None:
                normalized_tokens[index] = canonical

    @staticmethod
    def _is_initial(token: str) -> bool:
        return bool(re.fullmatch(r"(?:[a-z]\.){1,3}", token))

    @staticmethod
    def _match_key(token: str) -> str:
        return _split_outer_punctuation(token).core.lower()


def normalize_name(name: Optional[str], config: Optional[NameCaseConfig] = None) -> Optional[str]:
    """Convenience function around :class:`NameCaseEngine`."""

    return NameCaseEngine(config=config).normalize(name)
