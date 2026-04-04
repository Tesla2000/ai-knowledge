from __future__ import annotations

from pathlib import Path
from typing import Literal

from files._base import FileBase
from files._types import FileType
from pydantic.alias_generators import to_snake


class StubGenerationWorkflow(FileBase):
    type: Literal[FileType.STUB_GENERATION_WORKFLOW] = (
        FileType.STUB_GENERATION_WORKFLOW
    )
    stub_directory: str | None = None
    relative_path: Path = Path(".github/workflows/generate-stubs.yml")
    content: str = ""

    def _get_content(self, project_root: Path) -> str:
        directory = self.stub_directory or to_snake(project_root.name)
        return f"""\
name: Generate Stubs

permissions:
  contents: write

on:
  push:
    branches: [main]
  pull_request:
    branches:
      - "**"

jobs:
  generate_stubs:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install uv
        uses: astral-sh/setup-uv@v5

      - name: Install dependencies
        run: uv sync --group stubs

      - name: Generate stubs
        run: uv run python -m mypy.stubgen -p {directory} -o .

      - name: Verify stubs with mypy
        run: uv run mypy {directory}

      - name: Commit stubs
        if: github.event_name == 'push'
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git stash --include-untracked
          git pull --rebase origin main
          git stash pop
          git add {directory}
          git diff --cached --quiet || git commit -m "chore: regenerate stubs for {directory}"
          git push origin main
"""
