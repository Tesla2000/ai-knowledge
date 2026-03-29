from __future__ import annotations

from pathlib import Path
from typing import Literal

from files._base import FileBase
from files._types import FileType
from pydantic.alias_generators import to_snake


class PackageInitPy(FileBase):
    type: Literal[FileType.INIT_PY] = FileType.INIT_PY
    relative_path: Path = Path("__init__.py")
    content: str = ""

    def get_path(self, project_root: Path) -> Path:
        return project_root / to_snake(project_root.name) / self.relative_path
