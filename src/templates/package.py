from __future__ import annotations

from typing import Literal, Optional

from pydantic import Field
from pydantic.alias_generators import to_snake

from src.files import (
    Dependency,
    PackagePyprojectToml,
    PythonVersion,
    PyTypedFile,
    ReadmeFile,
    TestsWorkflow,
    VersionPatchWorkflow,
)
from src.files._base import FileBase
from src.templates._base import Template
from src.templates._type import TemplateType


def _default_repo_name(data: dict[str, object]) -> str:
    description = data.get("description", "")
    assert isinstance(description, str)
    return to_snake(description).replace("_", "-")


def _default_pyproject_toml(data: dict[str, object]) -> PackagePyprojectToml:
    description = data["description"]
    assert isinstance(
        description, str
    ), f"{description=} is not an instance of str"
    return PackagePyprojectToml(
        description=description,
        dependency_groups={
            "stubs": (Dependency(name="mypy", constraint=">=1.19.1"),)
        },
    )


def _default_readme(data: dict[str, object]) -> ReadmeFile:
    description = data["description"]
    assert isinstance(
        description, str
    ), f"{description=} is not an instance of str"
    author = data.get("author", "Tesla2000")
    repo_name = data.get("repo_name", "")
    badge = f"[![codecov](https://codecov.io/gh/{author}/{repo_name}/branch/main/graph/badge.svg)](https://codecov.io/gh/{author}/{repo_name})\n\n"
    return ReadmeFile(
        description=description,
        content=f"{badge}## Description\n\n$description\n",
    )


def _default_tests_workflow(data: dict[str, object]) -> TestsWorkflow:
    python_version = data.get("python_version", PythonVersion(minor=9))
    assert isinstance(python_version, PythonVersion)
    return TestsWorkflow(
        python_version=python_version,
        content=f"""\
name: Run tests

on:
  push:
    branches: [main]
  pull_request:
    branches:
      - "**"

jobs:
  test:
    name: Run Tests
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repo
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "{python_version}"

      - name: Install uv
        uses: astral-sh/setup-uv@v5

      - name: Install dependencies
        run: uv sync --group test

      - name: Run tests
        run: |
          timeout 69 uv run python -m pytest --cov --cov-report=term-missing --cov-report=xml --junitxml=junit.xml -o junit_family=legacy

      - name: Upload coverage reports to Codecov
        uses: codecov/codecov-action@v5
        with:
          token: ${{{{ secrets.CODECOV_TOKEN }}}}
""",
    )


class PythonPackage(Template):
    type: Literal[TemplateType.PACKAGE] = TemplateType.PACKAGE
    description: str
    author: str = "Tesla2000"
    repo_name: str = Field(default_factory=_default_repo_name)
    pyproject_toml: Optional[PackagePyprojectToml] = Field(
        default_factory=_default_pyproject_toml
    )
    readme: Optional[ReadmeFile] = Field(default_factory=_default_readme)
    tests_workflow: Optional[TestsWorkflow] = Field(
        default_factory=_default_tests_workflow
    )
    version_patch_workflow: Optional[VersionPatchWorkflow] = (
        VersionPatchWorkflow()
    )
    py_typed_file: Optional[PyTypedFile] = PyTypedFile()

    @property
    def files(self) -> tuple[FileBase, ...]:
        return tuple(
            filter(
                None,
                (
                    self.pyproject_toml,
                    *super().files,
                    self.version_patch_workflow,
                    self.py_typed_file,
                ),
            )
        )
