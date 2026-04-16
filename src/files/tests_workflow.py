from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import Field

from src.files._base import FileBase
from src.files._types import FileType


class TestsWorkflow(FileBase):
    type: Literal[FileType.TESTS_WORKFLOW] = FileType.TESTS_WORKFLOW
    relative_path: Path = Path(".github/workflows/tests.yml")
    python_version: str = "3.12"
    content: str = Field(default_factory=lambda validated_data: f"""\
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
    steps:
      - name: Checkout repo
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "{validated_data.get('python_version', '3.12')}"

      - name: Install uv
        uses: astral-sh/setup-uv@v5

      - name: Install dependencies
        run: uv sync

      - name: Run tests
        run: |
          timeout 69 uv run python -m unittest
""")
