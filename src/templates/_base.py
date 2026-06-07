from __future__ import annotations

from abc import ABC
from contextlib import ExitStack
from pathlib import Path

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


def _default_readme(data: dict[str, object]) -> ReadmeFile | None:
    description = data.get("description")
    if not isinstance(description, str):
        return None
    python_version = data.get("python_version")
    if not isinstance(python_version, PythonVersion):
        raise ValueError(
            f"{python_version=} is not an instance of {PythonVersion.__name__}"
        )
    return ReadmeFile(description=description, python_version=python_version)


def _default_python_version_file(
    data: dict[str, object],
) -> PythonVersionFile:
    python_version = data["python_version"]
    if not isinstance(python_version, PythonVersion):
        raise ValueError(
            f"{python_version=} is not an instance of {PythonVersion.__name__}"
        )
    return PythonVersionFile(python_version=python_version)


def _default_pre_commit_config(
    data: dict[str, object],
) -> PreCommitConfig:
    python_version = data["python_version"]
    if not isinstance(python_version, PythonVersion):
        raise ValueError(
            f"{python_version=} is not an instance of {PythonVersion.__name__}"
        )
    return PreCommitConfig(python_version=python_version)


class Template(BaseModel, ABC):
    type: TemplateType
    description: str | None = None
    python_version: PythonVersion = PythonVersion(minor=12)
    author: str = "Tesla2000"
    repo_name: str
    license: MitLicense | None = MitLicense()
    readme: ReadmeFile | None = Field(default_factory=_default_readme)
    pre_commit_run_workflow: PreCommitRunWorkflow | None = PreCommitRunWorkflow()
    tests_workflow: TestsWorkflow | None = TestsWorkflow()
    code_owners_file: CodeOwnersFile | None = CodeOwnersFile()
    pre_commit_config: PreCommitConfig | None = Field(
        default_factory=_default_pre_commit_config
    )
    setup_script: SetupScript | None = SetupScript()
    env_file: File | None = File(relative_path=Path(".env"), content="")
    python_version_file: PythonVersionFile | None = Field(
        default_factory=_default_python_version_file
    )
    gitignore: Gitignore | None = Gitignore()
    package_file: PackageFile | None = PackageFile()
    tests_init_file: File | None = File(
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
