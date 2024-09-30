from __future__ import annotations
from pydantic import BaseModel, ConfigDict
from typing import Pattern
from pathlib import Path


class Config(BaseModel):
    model_config = ConfigDict(validate_default=True)

    inputs_glob: list[str] = ["*.py"]
    tests_glob: list[str] = ["test_*.py"]
    tests_pattern: Pattern = "test_(.*).py"

    excluded_files: list[str] = ["__init__.py"]


class Paths(BaseModel):
    sources: Path
    tests: Path
