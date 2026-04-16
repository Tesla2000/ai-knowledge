from __future__ import annotations

from pathlib import Path
from typing import Annotated, Literal

from pydantic import Field

from src.files._base import FileBase
from src.files._types import FileType

PythonVersion = Annotated[str, Field(pattern=r"^\d+\.\d+(\.\d+)?$")]


class PythonVersionFile(FileBase):
    type: Literal[FileType.PYTHON_VERSION] = FileType.PYTHON_VERSION
    relative_path: Path = Path(".python-version")
    python_version: PythonVersion
    content: str = ""

    def _get_content(self, _: Path) -> str:
        return self.python_version
