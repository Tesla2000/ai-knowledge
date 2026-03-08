from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic.alias_generators import to_snake

from files._types import FileTypes
from files.file import File


class PackageInitPy(File):
    type: Literal[FileTypes.INIT_PY] = FileTypes.INIT_PY
    relative_path: Path = Path("__init__.py")
    content: str = ""

    def get_path(self, project_root: Path) -> Path:
        return project_root / to_snake(project_root.name) / self.relative_path
