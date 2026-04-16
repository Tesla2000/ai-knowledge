from typing import Annotated, Union

from pydantic import Discriminator

from src.files.code_owners_file import CodeOwnersFile
from src.files.file import File
from src.files.mit_license import MitLicense
from src.files.package_init_py import PackageFile
from src.files.package_pyproject_toml import Dependency, PackagePyprojectToml
from src.files.pre_commit_config import PreCommitConfig
from src.files.pre_commit_run_workflow import PreCommitRunWorkflow
from src.files.py_typed_file import PyTypedFile
from src.files.python_version_file import PythonVersionFile
from src.files.readme import ReadmeFile
from src.files.setup_script import SetupScript
from src.files.test_import_file import TestImportFile
from src.files.tests_workflow import TestsWorkflow
from src.files.version_patch_workflow import VersionPatchWorkflow

AnyFile = Annotated[
    Union[
        File,
        PackageFile,
        MitLicense,
        PackagePyprojectToml,
        PreCommitConfig,
        ReadmeFile,
        TestImportFile,
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
    "TestImportFile",
    "TestsWorkflow",
    "SetupScript",
    "VersionPatchWorkflow",
    "PreCommitRunWorkflow",
    "PackageFile",
    "PythonVersionFile",
    "PyTypedFile",
    "CodeOwnersFile",
    "AnyFile",
    "Dependency",
]
