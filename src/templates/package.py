from __future__ import annotations

from typing import Literal

from pydantic import Field

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


def _default_pyproject_toml(data: dict[str, object]) -> PackagePyprojectToml:
    description = data["description"]
    if not isinstance(description, str):
        raise ValueError(f"{description=} is not an instance of str")
    return PackagePyprojectToml(
        description=description,
        dependency_groups={"stubs": (Dependency(name="mypy", constraint=">=1.19.1"),)},
    )


def _default_readme(data: dict[str, object]) -> ReadmeFile:
    description = data["description"]
    if not isinstance(description, str):
        raise ValueError(f"{description=} is not an instance of str")
    author = data.get("author")
    repo_name = data.get("repo_name")
    python_version = data.get("python_version", PythonVersion(minor=9))
    if not isinstance(python_version, PythonVersion):
        raise ValueError(
            f"{python_version=} is not an instance of {PythonVersion.__name__}"
        )
    return ReadmeFile(
        description=description,
        github_owner=author,
        github_repo=repo_name,
        python_version=python_version,
    )


def _default_tests_workflow(data: dict[str, object]) -> TestsWorkflow:
    python_version = data.get("python_version", PythonVersion(minor=9))
    if not isinstance(python_version, PythonVersion):
        raise ValueError(
            f"{python_version=} is not an instance of {PythonVersion.__name__}"
        )
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
    pyproject_toml: PackagePyprojectToml | None = Field(
        default_factory=_default_pyproject_toml
    )
    readme: ReadmeFile | None = Field(default_factory=_default_readme)
    tests_workflow: TestsWorkflow | None = Field(
        default_factory=_default_tests_workflow
    )
    version_patch_workflow: VersionPatchWorkflow | None = VersionPatchWorkflow()
    py_typed_file: PyTypedFile | None = PyTypedFile()

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
