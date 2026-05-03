from typing import Annotated, Union

from pydantic import Discriminator

from src.files.file import File
from src.files.github.code_owners_file import CodeOwnersFile
from src.files.github.workflows.pre_commit_run_workflow import (
    PreCommitRunWorkflow,
)
from src.files.github.workflows.tests_workflow import TestsWorkflow
from src.files.github.workflows.version_patch_workflow import (
    VersionPatchWorkflow,
)
from src.files.gitignore import Gitignore
from src.files.mit_license import MitLicense
from src.files.package_pyproject_toml import Dependency, PackagePyprojectToml
from src.files.pre_commit_config import PreCommitConfig
from src.files.py_typed_file import PyTypedFile
from src.files.python_version_file import PythonVersion, PythonVersionFile
from src.files.readme import ReadmeFile
from src.files.setup_script import SetupScript
from src.files.src.package_init_py import PackageFile

AnyFile = Annotated[
    Union[
        File,
        PackageFile,
        MitLicense,
        Gitignore,
        PackagePyprojectToml,
        PreCommitConfig,
        ReadmeFile,
        TestsWorkflow,
        SetupScript,
        VersionPatchWorkflow,
        PreCommitRunWorkflow,
        PyTypedFile,
        CodeOwnersFile,
        PythonVersionFile,
    ],
    Discriminator("type"),
]

__all__ = [
    "File",
    "MitLicense",
    "PackagePyprojectToml",
    "PreCommitConfig",
    "ReadmeFile",
    "TestsWorkflow",
    "SetupScript",
    "VersionPatchWorkflow",
    "PreCommitRunWorkflow",
    "PackageFile",
    "PythonVersion",
    "PythonVersionFile",
    "PyTypedFile",
    "CodeOwnersFile",
    "Gitignore",
    "AnyFile",
    "Dependency",
]
