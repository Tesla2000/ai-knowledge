from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic.alias_generators import to_snake

from src.files._base import FileBase
from src.files._types import FileType


class PyTypedFile(FileBase):
    type: Literal[FileType.PY_TYPED] = FileType.PY_TYPED
    relative_path: Path = Path("py.typed")
    content: str = ""

    def get_path(self, project_root: Path) -> Path:
        return project_root / to_snake(project_root.name) / self.relative_path
