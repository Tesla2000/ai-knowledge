from __future__ import annotations

from pathlib import Path
from string import Template
from typing import Literal

from files._types import FileTypes
from files.file import File


class ReadmeFile(File):
    type: Literal[FileTypes.README] = FileTypes.README
    relative_path: Path = Path("README.md")
    description: str
    content: str = """\
## Description

$description
"""

    def _get_content(self, project_root: Path) -> str:
        return Template(self.content).safe_substitute(description=self.description)
