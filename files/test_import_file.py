from __future__ import annotations

from pathlib import Path
from string import Template
from typing import Literal

from files._base import FileBase
from files._types import FileType
from pydantic.alias_generators import to_snake


class TestImportFile(FileBase):
    type: Literal[FileType.TEST] = FileType.TEST
    relative_path: Path = Path("tests/test_import.py")
    script_name: str | None = None
    content: str = """\
from unittest import TestCase


class TestImport(TestCase):
    @staticmethod
    def test_import():
        import $script_name  # ignore

        _ = $script_name
"""

    def _get_content(self, project_root: Path) -> str:
        return Template(self.content).safe_substitute(
            script_name=self.script_name or to_snake(project_root.name),
        )
