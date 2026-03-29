from __future__ import annotations

from pathlib import Path
from typing import Literal

from files._base import FileBase
from files._types import FileType


class SetupScript(FileBase):
    type: Literal[FileType.SETUP_SCRIPT] = FileType.SETUP_SCRIPT
    relative_path: Path = Path("setup.sh")
    content: str = """\
#!/usr/bin/env bash
set -e

uv sync
pre-commit install --hook-type pre-commit --hook-type pre-push
"""
