# Global NameCase Engine

`global-namecase-engine` is a deterministic Python package for normalizing human names without depending on machine learning or external services.

It is designed for applications where predictability matters:

- API input normalization
- batch and ETL pipelines
- CRM or identity systems
- Django applications

## Why this package exists

Generic title-casing is not enough for personal names. Real-world inputs include particles, initials, apostrophes, generational suffixes, and culture-specific conventions that naive `.title()` logic breaks.

This package focuses on three things:

- deterministic output
- configurable rules
- a small, auditable codebase

## Installation

```bash
pip install global-namecase-engine
```

For Django integration:

```bash
pip install "global-namecase-engine[django]"
```

For local development:

```bash
pip install -e ".[dev]"
```

## Quick Start

```python
from global_namecase_engine import NameCaseEngine

engine = NameCaseEngine()

examples = [
    "JUAN DE LA CRUZ",
    "LUDWIG VAN BEETHOVEN",
    "O'CONNOR",
    "D'ANGELO",
    "ANNE-MARIE SMITH",
    "MARTIN LUTHER KING JR.",
    "R. NARAYANAN",
]

for raw in examples:
    print(f"{raw} -> {engine.normalize(raw)}")
```

Expected output:

```text
JUAN DE LA CRUZ -> Juan de la Cruz
LUDWIG VAN BEETHOVEN -> Ludwig van Beethoven
O'CONNOR -> O'Connor
D'ANGELO -> d'Angelo
ANNE-MARIE SMITH -> Anne-Marie Smith
MARTIN LUTHER KING JR. -> Martin Luther King Jr.
R. NARAYANAN -> R. Narayanan
```

## Supported Cases

- multi-word particles such as `de la`, `de los`, `van der`, and `von der`
- apostrophe names such as `O'Connor`, `N'Diaye`, and `d'Angelo`
- hyphenated names such as `Anne-Marie`
- initials such as `R.` or `J.R.R.`
- generational suffixes such as `Jr.` and `III`
- exception mappings for names that do not follow general rules
- whitespace cleanup and Unicode apostrophe normalization

## Customization

```python
from global_namecase_engine import NameCaseConfig, NameCaseEngine

config = NameCaseConfig(
    exceptions={
        "devito": "DeVito",
        "vanzandt": "VanZandt",
        "macarthur": "MacArthur",
    },
    lowercase_leading_particles=True,
)

engine = NameCaseEngine(config=config)

print(engine.normalize("DE NIRO"))
print(engine.normalize("MACARTHUR"))
```

## Django Integration

```python
from django.db import models

from global_namecase_engine.integrations.django import NameCaseField


class Person(models.Model):
    full_name = NameCaseField(max_length=200)
```

## Candidate Particle Discovery

The package includes a lightweight helper for discovering frequent middle tokens that may deserve review as new particles:

```python
from global_namecase_engine import discover_particles

names = [
    "Juan de la Cruz",
    "Maria de los Santos",
    "Ludwig van Beethoven",
    "Jan van der Meer",
]

print(discover_particles(names, min_count=2))
```

This helper is heuristic only. It is useful for building review queues, not for automatic rule acceptance.

## Development

Run the test suite:

```bash
python -m unittest discover -s tests -p "test_*.py"
```

Build the package:

```bash
python -m build
```

## Current Limits

This package is intentionally conservative. Some naming systems are too ambiguous for a safe universal rule.

- `Mac...` names are not aggressively rewritten by default because that creates false positives such as `Machado -> MacHado`.
- Leading particles such as `de Niro` are configurable because lowercasing the first token can also break given names such as `Van Morrison`.
- East Asian surname-first formatting is out of scope for now.

## Recommended Next Steps For Release

- choose and add an explicit open-source license
- add CI for tests, build, and publishing checks
- benchmark against a curated multilingual fixture set
- publish a versioned changelog before the first public release
