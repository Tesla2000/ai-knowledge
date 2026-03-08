from __future__ import annotations

from pathlib import Path
from typing import Any
from typing import Literal

from files import AnyFile
from files import File
from files import MitLicense
from files import PackageInitPy
from files import PackagePyprojectToml
from files import PreCommitConfig
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
    return (
        MitLicense(),
        PackagePyprojectToml(description=validated_data["description"]),
        ReadmeFile(description=validated_data["description"]),
        TestImportFile(),
        VersionPatchWorkflow(),
        TestsWorkflow(),
        PreCommitConfig(),
        SetupScript(),
        File(relative_path=Path(".env"), content=""),
        File(
            relative_path=Path(".gitignore"),
            content="/sandbox.py\n/.idea\n/.env\n/.venv\n/.vscode\n/.run/\n*__pycache__\n/docs/build/\n",
        ),
        PackageInitPy(),
        File(relative_path=Path("tests/__init__.py"), content=""),
    )


class _DescriptionMixin(BaseModel):
    description: str


class PythonPackage(Template, _DescriptionMixin):
    type: Literal[TemplateType.PACKAGE] = TemplateType.PACKAGE
    files: tuple[AnyFile, ...] = Field(default_factory=_generate_default_files)
