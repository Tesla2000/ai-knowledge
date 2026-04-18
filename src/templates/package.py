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
    PyTypedFile,
    ReadmeFile,
    SetupScript,
    TestImportFile,
    TestsWorkflow,
    VersionPatchWorkflow,
)
from src.templates._base import Template
from src.templates._type import TemplateType


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
            dependency_groups={
                "stubs": (Dependency(name="mypy", constraint=">=1.19.1"),)
            },
        ),
        ReadmeFile(description=description),
        TestImportFile(),
        VersionPatchWorkflow(),
        PreCommitRunWorkflow(),
        TestsWorkflow(),
        CodeOwnersFile(),
        PreCommitConfig(),
        SetupScript(),
        File(relative_path=Path(".env"), content=""),
        PythonVersionFile(python_version="3.12"),
        File(
            relative_path=Path(".gitignore"),
            content="/sandbox.py\n/.idea\n/.env\n/.venv\n/.vscode\n/.run/\n*__pycache__\n/docs/build/\n",
        ),
        PackageFile(),
        PyTypedFile(),
        File(relative_path=Path("tests/__init__.py"), content=""),
    ]
    if license_ := validated_data["license"]:
        assert isinstance(
            license_, MitLicense
        ), f"{license_=} is not an instance of {MitLicense.__name__}"
        files.append(license_)
    return tuple(files)


class _PythonPackageMixin(BaseModel):
    description: str
    license: Optional[MitLicense] = MitLicense()


class PythonPackage(Template, _PythonPackageMixin):
    type: Literal[TemplateType.PACKAGE] = TemplateType.PACKAGE
    files: tuple[AnyFile, ...] = Field(default_factory=_generate_default_files)
