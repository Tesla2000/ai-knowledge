from __future__ import annotations

from pathlib import Path
from typing import Annotated
from typing import Literal

from files._base import FileBase
from files._types import FileType
from pydantic import Field

PythonVersion = Annotated[str, Field(pattern=r"^\d+\.\d+(\.\d+)?$")]


class PythonVersionFile(FileBase):
    type: Literal[FileType.PYTHON_VERSION] = FileType.PYTHON_VERSION
    relative_path: Path = Path(".python-version")
    python_version: PythonVersion
    content: str = ""

    def _get_content(self, _: Path) -> str:
        return self.python_version
