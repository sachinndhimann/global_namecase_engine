"""Configuration objects and default rules for name normalization."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, FrozenSet, Iterable, Mapping, Tuple

ParticlePhrase = Tuple[str, ...]

DEFAULT_PARTICLE_PHRASES: FrozenSet[ParticlePhrase] = frozenset(
    {
        ("al",),
        ("bin",),
        ("bint",),
        ("da",),
        ("das",),
        ("de",),
        ("de", "la"),
        ("de", "las"),
        ("de", "los"),
        ("del",),
        ("des",),
        ("di",),
        ("do",),
        ("dos",),
        ("du",),
        ("el",),
        ("ibn",),
        ("la",),
        ("le",),
        ("van",),
        ("van", "de"),
        ("van", "den"),
        ("van", "der"),
        ("von",),
        ("von", "den"),
        ("von", "der"),
    }
)

DEFAULT_EXCEPTIONS: Dict[str, str] = {
    "devito": "DeVito",
    "vanzandt": "VanZandt",
}

DEFAULT_LOWERCASE_APOSTROPHE_PREFIXES: FrozenSet[str] = frozenset({"d", "l"})
DEFAULT_TITLECASE_APOSTROPHE_PREFIXES: FrozenSet[str] = frozenset({"o"})

DEFAULT_SUFFIXES: Dict[str, str] = {
    "dds": "DDS",
    "esq": "Esq.",
    "esq.": "Esq.",
    "ii": "II",
    "iii": "III",
    "iv": "IV",
    "ix": "IX",
    "jr": "Jr.",
    "jr.": "Jr.",
    "m.d.": "M.D.",
    "md": "MD",
    "ph.d.": "Ph.D.",
    "phd": "PhD",
    "sr": "Sr.",
    "sr.": "Sr.",
    "v": "V",
    "vi": "VI",
    "vii": "VII",
    "viii": "VIII",
    "x": "X",
}


@dataclass(slots=True)
class NameCaseConfig:
    """Configuration for deterministic name normalization."""

    particle_phrases: FrozenSet[ParticlePhrase] = DEFAULT_PARTICLE_PHRASES
    exceptions: Mapping[str, str] = field(default_factory=lambda: dict(DEFAULT_EXCEPTIONS))
    lowercase_apostrophe_prefixes: FrozenSet[str] = DEFAULT_LOWERCASE_APOSTROPHE_PREFIXES
    titlecase_apostrophe_prefixes: FrozenSet[str] = DEFAULT_TITLECASE_APOSTROPHE_PREFIXES
    suffixes: Mapping[str, str] = field(default_factory=lambda: dict(DEFAULT_SUFFIXES))
    lowercase_leading_particles: bool = False

    def with_additional_particles(
        self,
        particle_phrases: Iterable[ParticlePhrase],
    ) -> "NameCaseConfig":
        return NameCaseConfig(
            particle_phrases=self.particle_phrases.union(set(particle_phrases)),
            exceptions=dict(self.exceptions),
            lowercase_apostrophe_prefixes=self.lowercase_apostrophe_prefixes,
            titlecase_apostrophe_prefixes=self.titlecase_apostrophe_prefixes,
            suffixes=dict(self.suffixes),
            lowercase_leading_particles=self.lowercase_leading_particles,
        )
