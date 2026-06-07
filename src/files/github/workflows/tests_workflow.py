from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import Field

from src.files._base import FileBase
from src.files._types import FileType
from src.files.python_version_file import PythonVersion


def _content(validated_data: dict[str, object]) -> str:
    python_version = validated_data.get("python_version", PythonVersion(minor=12))
    if not isinstance(python_version, PythonVersion):
        raise ValueError(
            f"{python_version=} is not an instance of {PythonVersion.__name__}"
        )
    matrix_versions = ", ".join(
        f'"3.{minor}"' for minor in range(python_version.minor, 15)
    )
    return f"""\
name: Run tests

on:
  push:
    branches: [main]
  pull_request:
    branches:
      - "**"

jobs:
  test:
    name: Run Tests
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [{matrix_versions}]
    steps:
      - name: Checkout repo
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{{{ matrix.python-version }}}}

      - name: Install uv
        uses: astral-sh/setup-uv@v5

      - name: Install dependencies
        run: uv sync --group test

      - name: Run tests
        run: |
          timeout 69 uv run python -m pytest --cov --cov-report=term-missing -m "not smoke"
"""


class TestsWorkflow(FileBase):
    type: Literal[FileType.TESTS_WORKFLOW] = FileType.TESTS_WORKFLOW
    relative_path: Path = Path(".github/workflows/tests.yml")
    python_version: PythonVersion = PythonVersion(minor=12)
    content: str = Field(default_factory=_content)
