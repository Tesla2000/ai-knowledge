from __future__ import annotations

from pathlib import Path
from typing import Literal

from files._types import FileTypes
from files.file import File


class SetupScript(File):
    type: Literal[FileTypes.SETUP_SCRIPT] = FileTypes.SETUP_SCRIPT
    relative_path: Path = Path("setup.sh")
    content: str = """\
#!/usr/bin/env bash
set -e

uv sync
git init
pre-commit install --hook-type pre-commit --hook-type pre-push
pre-commit autoupdate
git add .
git commit -m "initial commit"
"""
