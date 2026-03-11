"""Minimal PEP 517 backend for building this pure-Python package."""

from __future__ import annotations

import base64
import csv
import hashlib
import io
import tarfile
import zipfile
from pathlib import Path
from typing import Iterable, List, Sequence, Tuple

NAME = "global-namecase-engine"
VERSION = "0.2.0"
SUMMARY = "Deterministic, configurable human-name casing for Python applications."
PYTHON_REQUIRES = ">=3.9"
PACKAGE_NAME = "global_namecase_engine"
DIST_NAME = NAME.replace("-", "_")
DIST_INFO = f"{DIST_NAME}-{VERSION}.dist-info"
ROOT = Path(__file__).resolve().parent

CLASSIFIERS: Sequence[str] = (
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3 :: Only",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Text Processing :: Linguistic",
)

OPTIONAL_DEPENDENCIES = {
    "django": ["Django>=4.2"],
    "dev": ["build>=1.2", "pytest>=8.0", "twine>=5.0"],
}


def _metadata_text() -> str:
    lines = [
        "Metadata-Version: 2.1",
        f"Name: {NAME}",
        f"Version: {VERSION}",
        f"Summary: {SUMMARY}",
        f"Requires-Python: {PYTHON_REQUIRES}",
        "Keywords: name casing, name normalization, identity, etl, django",
    ]
    lines.extend(f"Classifier: {classifier}" for classifier in CLASSIFIERS)
    for extra, requirements in OPTIONAL_DEPENDENCIES.items():
        lines.append(f"Provides-Extra: {extra}")
        for requirement in requirements:
            lines.append(f"Requires-Dist: {requirement}; extra == '{extra}'")
    lines.append("")
    return "\n".join(lines)


def _wheel_text() -> str:
    return "\n".join(
        [
            "Wheel-Version: 1.0",
            "Generator: global_namecase_engine.build_backend",
            "Root-Is-Purelib: true",
            "Tag: py3-none-any",
            "",
        ]
    )


def _top_level_text() -> str:
    return f"{PACKAGE_NAME}\n"


def _iter_package_files() -> Iterable[Path]:
    package_root = ROOT / PACKAGE_NAME
    for path in sorted(package_root.rglob("*")):
        if path.is_dir():
            continue
        if "__pycache__" in path.parts:
            continue
        yield path


def _iter_sdist_files() -> Iterable[Path]:
    for relative_path in ("README.md", "build_backend.py", "pyproject.toml"):
        yield ROOT / relative_path
    for path in sorted((ROOT / "tests").rglob("*")):
        if path.is_file() and "__pycache__" not in path.parts:
            yield path
    yield from _iter_package_files()


def _hash_bytes(data: bytes) -> str:
    digest = hashlib.sha256(data).digest()
    return base64.urlsafe_b64encode(digest).decode("ascii").rstrip("=")


def _record_text(entries: Sequence[Tuple[str, bytes]], record_path: str) -> str:
    output = io.StringIO()
    writer = csv.writer(output, lineterminator="\n")
    for path, data in entries:
        writer.writerow((path, f"sha256={_hash_bytes(data)}", str(len(data))))
    writer.writerow((record_path, "", ""))
    return output.getvalue()


def _metadata_entries() -> List[Tuple[str, bytes]]:
    return [
        (f"{DIST_INFO}/METADATA", _metadata_text().encode("utf-8")),
        (f"{DIST_INFO}/WHEEL", _wheel_text().encode("utf-8")),
        (f"{DIST_INFO}/top_level.txt", _top_level_text().encode("utf-8")),
    ]


def prepare_metadata_for_build_wheel(metadata_directory, config_settings=None) -> str:
    metadata_root = Path(metadata_directory) / DIST_INFO
    metadata_root.mkdir(parents=True, exist_ok=True)
    for relative_path, data in _metadata_entries():
        destination = Path(metadata_directory) / relative_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)
    return DIST_INFO


def build_wheel(wheel_directory, config_settings=None, metadata_directory=None) -> str:
    wheel_root = Path(wheel_directory)
    wheel_root.mkdir(parents=True, exist_ok=True)

    filename = f"{DIST_NAME}-{VERSION}-py3-none-any.whl"
    wheel_path = wheel_root / filename
    record_path = f"{DIST_INFO}/RECORD"

    entries: List[Tuple[str, bytes]] = []
    with zipfile.ZipFile(wheel_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in _iter_package_files():
            relative_path = path.relative_to(ROOT).as_posix()
            data = path.read_bytes()
            archive.writestr(relative_path, data)
            entries.append((relative_path, data))

        for relative_path, data in _metadata_entries():
            archive.writestr(relative_path, data)
            entries.append((relative_path, data))

        record_data = _record_text(entries, record_path).encode("utf-8")
        archive.writestr(record_path, record_data)

    return filename


def build_sdist(sdist_directory, config_settings=None) -> str:
    sdist_root = Path(sdist_directory)
    sdist_root.mkdir(parents=True, exist_ok=True)

    filename = f"{DIST_NAME}-{VERSION}.tar.gz"
    sdist_path = sdist_root / filename
    archive_root = f"{DIST_NAME}-{VERSION}"

    with tarfile.open(sdist_path, "w:gz") as archive:
        for path in _iter_sdist_files():
            relative_path = path.relative_to(ROOT).as_posix()
            archive.add(path, arcname=f"{archive_root}/{relative_path}")

    return filename


def get_requires_for_build_wheel(config_settings=None):
    return []


def get_requires_for_build_sdist(config_settings=None):
    return []
