from __future__ import annotations

from pathlib import Path
from string import Template
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr
from pydantic.alias_generators import to_snake

from src.files._base import FileBase
from src.files._types import FileType


class Dependency(BaseModel):
    model_config = ConfigDict(frozen=True)
    name: str
    constraint: str = ""

    def __str__(self) -> str:
        return f"{self.name}{self.constraint}"


class PackagePyprojectToml(FileBase):
    type: Literal[FileType.PYPROJECT_TOML] = FileType.PYPROJECT_TOML
    relative_path: Path = Path("pyproject.toml")
    project_name_low: str | None = None
    version: str = "0.1.0"
    description: str
    author_name: str = "Tesla2000"
    author_email: EmailStr = "fratajczak124@gmail.com"
    python_version: str = "3.9"
    dependencies: tuple[Dependency, ...] = ()
    dependency_groups: dict[str, tuple[Dependency, ...]] = {}
    content: str = """\
[project]
name = "$project_name_low"
version = "$version"
description = "$description"
authors = [{name = "$author_name", email = "$author_email"}]
readme = "README.md"
requires-python = ">=$python_version"
dependencies = $dependencies

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["$project_name_low"]

[tool.isort]
profile = "black"

[tool.mypy]
python_version = "3.12"
strict = true
plugins = ["pydantic.mypy"]
mypy_path = "stubs"
"""

    def _get_content(self, project_root: Path) -> str:
        if self.dependencies:
            deps_str = (
                "[\n"
                + "".join(f'    "{dep}",\n' for dep in self.dependencies)
                + "]"
            )
        else:
            deps_str = "[]"
        base = Template(self.content).safe_substitute(
            project_name_low=self.project_name_low
            or to_snake(project_root.name),
            version=self.version,
            description=self.description,
            author_name=self.author_name,
            author_email=self.author_email,
            python_version=self.python_version,
            dependencies=deps_str,
        )
        if not self.dependency_groups:
            return base
        groups_str = "\n[dependency-groups]\n"
        for group, deps in self.dependency_groups.items():
            group_deps = (
                "[\n" + "".join(f'    "{dep}",\n' for dep in deps) + "]"
            )
            groups_str += f"{group} = {group_deps}\n"
        return base + groups_str
