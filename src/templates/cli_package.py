from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Literal

from pydantic import Field

from src.files import (
    Dependency,
    PackageFile,
    PackagePyprojectToml,
    PreCommitConfig,
    PythonVersion,
)
from src.files._base import FileBase
from src.templates._base import Template
from src.templates._type import TemplateType

_CLI_MYPY_DEPS = (
    Dependency(name="pydantic", constraint=">=2.8.2"),
    Dependency(name="pydantic-settings", constraint=">=2.13.0"),
)

_MAIN_PY_CONTENT = """\
from pydantic_settings import BaseSettings
from pydantic_settings import CliApp
from pydantic_settings import SettingsConfigDict


class Main(BaseSettings):
    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        cli_parse_args=True,
        cli_kebab_case=True,
    )

    async def cli_cmd(self) -> None:
        pass


if __name__ == "__main__":  # pragma: no cover
    CliApp.run(Main)
"""


def _default_pyproject_toml(
    data: Mapping[str, object],  # ignore
) -> PackagePyprojectToml:
    description = data["description"]
    if not isinstance(description, str):
        msg = f"{description=} is not an instance of str"
        raise TypeError(msg)
    python_version = data["python_version"]
    if not isinstance(python_version, PythonVersion):
        msg = (
            f"{python_version=} is not an instance of {PythonVersion.__name__}"
        )
        raise TypeError(msg)
    return PackagePyprojectToml(
        description=description,
        dependencies=(
            Dependency(name="pydantic-settings", constraint=">=2.13.0"),
        ),
        python_version=python_version,
        dependency_groups={},
    )


def _default_pre_commit_config_cli(
    data: Mapping[str, object],  # ignore
) -> PreCommitConfig:
    python_version = data["python_version"]
    if not isinstance(python_version, PythonVersion):
        msg = (
            f"{python_version=} is not an instance of {PythonVersion.__name__}"
        )
        raise TypeError(msg)
    return PreCommitConfig(
        python_version=python_version,
        mypy_additional_dependencies=_CLI_MYPY_DEPS,
    )


class CliPackage(Template):
    type: Literal[TemplateType.CLI_PACKAGE] = TemplateType.CLI_PACKAGE
    description: str
    pyproject_toml: PackagePyprojectToml | None = Field(
        default_factory=_default_pyproject_toml
    )
    pre_commit_config: PreCommitConfig | None = Field(
        default_factory=_default_pre_commit_config_cli
    )
    main_py: PackageFile | None = PackageFile(
        relative_path=Path("__main__.py"), content=_MAIN_PY_CONTENT
    )

    @property
    def files(self) -> tuple[FileBase, ...]:
        return tuple(
            filter(
                None,
                (
                    self.pyproject_toml,
                    *super().files,
                    self.main_py,
                ),
            )
        )
