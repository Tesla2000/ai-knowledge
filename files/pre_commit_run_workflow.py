from __future__ import annotations

from pathlib import Path
from typing import Literal

from files._types import FileTypes
from files.file import File


class PreCommitRunWorkflow(File):
    type: Literal[FileTypes.PRE_COMMIT_RUN_WORKFLOW] = (
        FileTypes.PRE_COMMIT_RUN_WORKFLOW
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
