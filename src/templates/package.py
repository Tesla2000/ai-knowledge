from __future__ import annotations

from pathlib import Path
from typing import Any
from typing import Literal
from typing import Optional

from pydantic import BaseModel
from pydantic import Field

from src.files import AnyFile
from src.files import CodeOwnersFile
from src.files import Dependency
from src.files import File
from src.files import MitLicense
from src.files import PackageFile
from src.files import PackagePyprojectToml
from src.files import PreCommitConfig
from src.files import PreCommitRunWorkflow
from src.files import PythonVersionFile
from src.files import PyTypedFile
from src.files import ReadmeFile
from src.files import SetupScript
from src.files import TestImportFile
from src.files import TestsWorkflow
from src.files import VersionPatchWorkflow
from src.templates._base import Template
from src.templates._type import TemplateType


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
    if validated_data["license"]:
        files.append(validated_data["license"])
    return tuple(files)


class _PythonPackageMixin(BaseModel):
    description: str
    license: Optional[MitLicense] = MitLicense()


class PythonPackage(Template, _PythonPackageMixin):
    type: Literal[TemplateType.PACKAGE] = TemplateType.PACKAGE
    files: tuple[AnyFile, ...] = Field(default_factory=_generate_default_files)
