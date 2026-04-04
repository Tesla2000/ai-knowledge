from __future__ import annotations

from pathlib import Path
from typing import Any
from typing import Literal
from typing import Optional

from files import AnyFile
from files import Dependency
from files import File
from files import MitLicense
from files import PackageFile
from files import PackagePyprojectToml
from files import PreCommitConfig
from files import PreCommitRunWorkflow
from files import PythonVersionFile
from files import PyTypedFile
from files import ReadmeFile
from files import SetupScript
from files import TestImportFile
from files import TestsWorkflow
from files import VersionPatchWorkflow
from pydantic import BaseModel
from pydantic import Field
from templates._base import Template
from templates._type import TemplateType


def _generate_default_files(
    validated_data: dict[str, Any],
) -> tuple[AnyFile, ...]:
    if "description" not in validated_data:
        raise ValueError(f"Description not provided in {validated_data}")
    if "license" not in validated_data:
        raise ValueError(f"License not provided in {validated_data}")
    files: list[AnyFile] = [
        PackagePyprojectToml(
            description=validated_data["description"],
            dependency_groups={
                "stubs": (Dependency(name="mypy", constraint=">=1.19.1"),)
            },
        ),
        ReadmeFile(description=validated_data["description"]),
        TestImportFile(),
        VersionPatchWorkflow(),
        PreCommitRunWorkflow(),
        TestsWorkflow(),
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
    if validated_data["license"]:
        files.append(validated_data["license"])
    return tuple(files)


class _PythonPackageMixin(BaseModel):
    description: str
    license: Optional[MitLicense] = MitLicense()


class PythonPackage(Template, _PythonPackageMixin):
    type: Literal[TemplateType.PACKAGE] = TemplateType.PACKAGE
    files: tuple[AnyFile, ...] = Field(default_factory=_generate_default_files)
