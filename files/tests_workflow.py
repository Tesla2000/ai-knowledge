from __future__ import annotations

from pathlib import Path
from typing import Literal

from files._types import FileTypes
from files.file import File


class TestsWorkflow(File):
    type: Literal[FileTypes.TESTS_WORKFLOW] = FileTypes.TESTS_WORKFLOW
    relative_path: Path = Path(".github/workflows/tests.yml")
    content: str = """\
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
          python-version: "3.11"

      - name: Install uv
        uses: astral-sh/setup-uv@v5

      - name: Install dependencies
        run: uv sync

      - name: Run tests
        run: |
          timeout 7 uv run python -m unittest
"""
