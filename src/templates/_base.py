from __future__ import annotations

from abc import ABC
from contextlib import ExitStack
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field

from src.files import (
    CodeOwnersFile,
    File,
    Gitignore,
    MitLicense,
    PackageFile,
    PreCommitConfig,
    PreCommitRunWorkflow,
    PythonVersion,
    PythonVersionFile,
    ReadmeFile,
    SetupScript,
    TestsWorkflow,
)
from src.files._base import FileBase
from src.templates._type import TemplateType


def _default_readme(data: dict[str, object]) -> Optional[ReadmeFile]:
    description = data.get("description")
    if not isinstance(description, str):
        return None
    python_version = data.get("python_version")
    assert isinstance(python_version, PythonVersion)
    return ReadmeFile(description=description, python_version=python_version)


def _default_python_version_file(
    data: dict[str, object],
) -> PythonVersionFile:
    python_version = data["python_version"]
    assert isinstance(python_version, PythonVersion)
    return PythonVersionFile(python_version=python_version)


def _default_pre_commit_config(
    data: dict[str, object],
) -> PreCommitConfig:
    python_version = data["python_version"]
    assert isinstance(python_version, PythonVersion)
    return PreCommitConfig(python_version=python_version)


class Template(BaseModel, ABC):
    type: TemplateType
    description: Optional[str] = None
    python_version: PythonVersion = PythonVersion(minor=12)
    license: Optional[MitLicense] = MitLicense()
    readme: Optional[ReadmeFile] = Field(default_factory=_default_readme)
    pre_commit_run_workflow: Optional[PreCommitRunWorkflow] = (
        PreCommitRunWorkflow()
    )
    tests_workflow: Optional[TestsWorkflow] = TestsWorkflow()
    code_owners_file: Optional[CodeOwnersFile] = CodeOwnersFile()
    pre_commit_config: Optional[PreCommitConfig] = Field(
        default_factory=_default_pre_commit_config
    )
    setup_script: Optional[SetupScript] = SetupScript()
    env_file: Optional[File] = File(relative_path=Path(".env"), content="")
    python_version_file: Optional[PythonVersionFile] = Field(
        default_factory=_default_python_version_file
    )
    gitignore: Optional[Gitignore] = Gitignore()
    package_file: Optional[PackageFile] = PackageFile()
    tests_init_file: Optional[File] = File(
        relative_path=Path("tests/__init__.py"), content=""
    )

    @property
    def files(self) -> tuple[FileBase, ...]:
        return tuple(
            filter(
                None,
                (
                    self.readme,
                    self.pre_commit_run_workflow,
                    self.tests_workflow,
                    self.code_owners_file,
                    self.pre_commit_config,
                    self.setup_script,
                    self.env_file,
                    self.python_version_file,
                    self.gitignore,
                    self.package_file,
                    self.tests_init_file,
                    self.license,
                ),
            )
        )

    def generate(self, project_root: Path) -> None:
        with ExitStack() as stack:
            for file in self.files:
                stack.enter_context(file.revert_on_fail(project_root))
                file.write(project_root)
