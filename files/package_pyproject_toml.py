from __future__ import annotations

from pathlib import Path
from string import Template
from typing import Literal

from files._types import FileTypes
from files.file import File
from pydantic.alias_generators import to_snake


class PackagePyprojectToml(File):
    type: Literal[FileTypes.PYPROJECT_TOML] = FileTypes.PYPROJECT_TOML
    relative_path: Path = Path("pyproject.toml")
    project_name_low: str | None = None
    description: str
    content: str = """\
[project]
name = "$project_name_low"
version = "0.1.0"
description = "$description"
authors = [{name = "Tesla2000", email = "fratajczak124@gmail.com"}]
readme = "README.md"
requires-python = ">=3.9"
dependencies = []

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["$project_name_low"]
"""

    def _get_content(self, project_root: Path) -> str:
        return Template(self.content).safe_substitute(
            project_name_low=self.project_name_low
            or to_snake(project_root.name),
            description=self.description,
        )
