from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, PositiveInt

from src.files._base import FileBase
from src.files._types import FileType


class PythonVersion(BaseModel):
    model_config = ConfigDict(frozen=True)
    major: int = Field(3, ge=2, le=3)
    minor: PositiveInt
    patch: PositiveInt | None = None

    def __str__(self) -> str:
        base = f"{self.major}.{self.minor}"
        return base if self.patch is None else f"{base}.{self.patch}"


class PythonVersionFile(FileBase):
    type: Literal[FileType.PYTHON_VERSION] = FileType.PYTHON_VERSION
    relative_path: Path = Path(".python-version")
    python_version: PythonVersion
    content: str = ""

    def _get_content(self, _: Path) -> str:
        return str(self.python_version)
