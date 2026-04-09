from __future__ import annotations

from pathlib import Path
from typing import Literal

from src.files._base import FileBase
from src.files._types import FileType


class PreCommitRunWorkflow(FileBase):
    type: Literal[FileType.PRE_COMMIT_RUN_WORKFLOW] = (
        FileType.PRE_COMMIT_RUN_WORKFLOW
    )
    relative_path: Path = Path(".github/workflows/pre-commit.yml")
    content: str = """\
name: pre-commit

on:
  pull_request:
  push:
    branches: [main]

jobs:
  pre-commit:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4.1.1
    - uses: pre-commit/action@v3.0.0
      env:
        SKIP: vulture

"""
