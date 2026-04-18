from __future__ import annotations

from pathlib import Path
from typing import Literal, Optional

from pydantic import BaseModel, Field

from src.files import (
    AnyFile,
    CodeOwnersFile,
    Dependency,
    File,
    MitLicense,
    PackageFile,
    PackagePyprojectToml,
    PreCommitConfig,
    PreCommitRunWorkflow,
    PythonVersionFile,
    ReadmeFile,
    SetupScript,
    TestImportFile,
    TestsWorkflow,
)
from src.templates._base import Template
from src.templates._type import TemplateType

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


if __name__ == "__main__":
    CliApp.run(Main)
"""


def _generate_default_files(
    validated_data: dict[str, object],
) -> tuple[AnyFile, ...]:
    if "description" not in validated_data:
        raise ValueError(f"Description not provided in {validated_data}")
    if "license" not in validated_data:
        raise ValueError(f"License not provided in {validated_data}")
    description = validated_data["description"]
    assert isinstance(
        description, str
    ), f"{description=} is not an instance of str"
    files: list[AnyFile] = [
        PackagePyprojectToml(
            description=description,
            dependencies=(
                Dependency(name="pydantic-settings", constraint=">=2.13.0"),
            ),
            python_version="3.10",
            dependency_groups={
                "stubs": (Dependency(name="mypy", constraint=">=1.19.1"),)
            },
        ),
        ReadmeFile(description=description),
        TestImportFile(),
        PreCommitRunWorkflow(),
        TestsWorkflow(),
        PreCommitConfig(
            mypy_additional_dependencies=(
                Dependency(name="pydantic", constraint=">=2.8.2"),
                Dependency(name="pydantic-settings", constraint=">=2.13.0"),
            )
        ),
        SetupScript(),
        File(relative_path=Path(".env"), content=""),
        PythonVersionFile(python_version="3.12"),
        File(
            relative_path=Path(".gitignore"),
            content="/sandbox.py\n/.idea\n/.env\n/.venv\n/.vscode\n/.run/\n*__pycache__\n/docs/build/\n",
        ),
        CodeOwnersFile(),
        PackageFile(),
        PackageFile(
            relative_path=Path("__main__.py"), content=_MAIN_PY_CONTENT
        ),
        File(relative_path=Path("tests/__init__.py"), content=""),
    ]

    if license_ := validated_data["license"]:
        assert isinstance(
            license_, MitLicense
        ), f"{license_=} is not an instance of {MitLicense.__name__}"
        files.append(license_)
    return tuple(files)


class _CliPackageMixin(BaseModel):
    description: str
    license: Optional[MitLicense] = MitLicense()


class CliPackage(Template, _CliPackageMixin):
    type: Literal[TemplateType.CLI_PACKAGE] = TemplateType.CLI_PACKAGE
    files: tuple[AnyFile, ...] = Field(default_factory=_generate_default_files)
