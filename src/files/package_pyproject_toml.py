from __future__ import annotations

from pathlib import Path
from string import Template
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field
from pydantic.alias_generators import to_snake

from src.files._base import FileBase
from src.files._types import FileType
from src.files.python_version_file import PythonVersion


class Dependency(BaseModel):
    model_config = ConfigDict(frozen=True)
    name: str
    constraint: str = ""

    def __str__(self) -> str:
        return f"{self.name}{self.constraint}"


def _default_classifiers(
    data: dict[str, object],  # ignore
) -> tuple[str, ...]:
    python_version = data.get("python_version")
    min_minor = (
        python_version.minor
        if isinstance(python_version, PythonVersion)
        else 9
    )
    return (
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        *(
            f"Programming Language :: Python :: 3.{minor}"
            for minor in range(min_minor, 15)
        ),
        "Typing :: Typed",
    )


class PackagePyprojectToml(FileBase):
    type: Literal[FileType.PYPROJECT_TOML] = FileType.PYPROJECT_TOML
    relative_path: Path = Path("pyproject.toml")
    project_name_low: str | None = None
    version: str = "0.1.0"
    description: str
    author_name: str = "Tesla2000"
    author_email: EmailStr = "fratajczak124@gmail.com"
    python_version: PythonVersion = PythonVersion(minor=9)
    dependencies: tuple[Dependency, ...] = ()
    dependency_groups: dict[str, tuple[Dependency, ...]] = Field(
        default_factory=dict
    )
    classifiers: tuple[str, ...] = Field(default_factory=_default_classifiers)
    content: str = """\
[project]
name = "$project_name_low"
version = "$version"
description = "$description"
authors = [{name = "$author_name", email = "$author_email"}]
readme = "README.md"
requires-python = ">=$python_version"
dependencies = $dependencies
classifiers = $classifiers

[project.urls]
Homepage = "https://github.com/$author_name/$github_repo_name"
Issues = "https://github.com/$author_name/$github_repo_name/issues"
Coverage = "https://codecov.io/gh/$author_name/$github_repo_name"

[dependency-groups]
test = [
    "pytest>=8.4.2",
    "pytest-cov>=7.1.0",
    "pytest-logger>=1.1.1",
]
dev = [
    {include-group = "test"},
    "mypy",
    "pre-commit"
]
$dependency_groups


[tool.coverage.run]
branch = true
source = ["$project_name_low"]

[tool.coverage.report]
fail_under = 100
show_missing = true
skip_covered = true

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["$project_name_low"]

[tool.ruff]
line-length = 79

[tool.ruff.lint]
select = ["ALL"]
ignore = ["D", "E501", "S101", "S603", "S607", "COM812", "EM102", "TRY003", "TC001", "TC002", "TC003"]

[tool.pytest.ini_options]
markers = [
    "unit: tests that exercise a single component in isolation",
    "integration: tests that verify multiple components work together",
    "e2e: tests that exercise the full pipeline against real external services",
    "smoke: quick sanity check that the basic pipeline runs",
    "manual: tests that require manual interaction or setup",
]
log_cli = false
log_cli_level = "DEBUG"
log_format = "%(asctime)s [%(levelname)8s] %(message)s"
log_date_format = "%Y-%m-%d %H:%M:%S"

[tool.mypy]
python_version = "$python_version"
strict = true
$mypy_plugins
mypy_path = "stubs"
"""

    def _get_content(self, project_root: Path) -> str:
        project_name_low = self.project_name_low or to_snake(project_root.name)
        deps_str = (
            "[\n"
            + "".join(f'    "{dep}",\n' for dep in self.dependencies)
            + "]"
            if self.dependencies
            else "[]"
        )
        dependency_groups = "".join(
            f"{group} = [\n"
            + "".join(f'    "{dep}",\n' for dep in deps)
            + "]\n"
            for group, deps in self.dependency_groups.items()
        )
        classifiers_str = (
            "[\n" + "".join(f'    "{c}",\n' for c in self.classifiers) + "]"
        )
        mypy_plugins = (
            'plugins = ["pydantic.mypy"]'
            if any(dep.name == "pydantic" for dep in self.dependencies)
            else ""
        )
        return Template(self.content).safe_substitute(
            project_name_low=project_name_low,
            github_repo_name=project_name_low.replace("_", "-"),
            version=self.version,
            description=self.description,
            author_name=self.author_name,
            author_email=self.author_email,
            python_version=self.python_version,
            dependencies=deps_str,
            dependency_groups=dependency_groups,
            classifiers=classifiers_str,
            mypy_plugins=mypy_plugins,
        )
