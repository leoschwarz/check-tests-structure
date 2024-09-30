from __future__ import annotations

import tomllib
from pathlib import Path
from typing import Pattern

from pydantic import BaseModel, ConfigDict


class Config(BaseModel):
    model_config = ConfigDict(validate_default=True)

    sources_path: Path
    tests_path: Path

    inputs_glob: list[str] = ["*.py"]
    tests_glob: list[str] = ["test_*.py"]
    tests_pattern: Pattern = "test_(.*).py"

    allow_missing_sources: bool = False
    allow_missing_tests: bool = False

    excluded_files: list[str] = ["__init__.py", "__main__.py"]


def find_pyproject_toml(path: Path) -> Path | None:
    """Searches for the pyproject.toml file in the given path or any of its parent directories."""
    while not (path / "pyproject.toml").exists():
        if path == path.parent:
            break
        path = path.parent
    if (path / "pyproject.toml").exists():
        return path / "pyproject.toml"
    else:
        return None


def parse_pyproject_toml(path: Path) -> Config:
    metadata = tomllib.loads(path.read_text())
    return Config.model_validate(
        metadata.get("tool", {}).get("check-tests-structure", {})
    )
