"""Public package interface for global_namecase_engine."""

from .config import NameCaseConfig
from .engine import NameCaseEngine, normalize_name
from .learning import discover_particles

__all__ = [
    "NameCaseConfig",
    "NameCaseEngine",
    "discover_particles",
    "normalize_name",
]
