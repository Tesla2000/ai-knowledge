from typing import Annotated
from typing import Union

from files.file import File
from files.mit_license import MitLicense
from files.package_init_py import PackageFile
from files.package_pyproject_toml import Dependency
from files.package_pyproject_toml import PackagePyprojectToml
from files.pre_commit_config import PreCommitConfig
from files.pre_commit_run_workflow import PreCommitRunWorkflow
from files.py_typed_file import PyTypedFile
from files.python_version_file import PythonVersionFile
from files.readme import ReadmeFile
from files.setup_script import SetupScript
from files.stub_generation_workflow import StubGenerationWorkflow
from files.test_import_file import TestImportFile
from files.tests_workflow import TestsWorkflow
from files.version_patch_workflow import VersionPatchWorkflow
from pydantic import Discriminator

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
        StubGenerationWorkflow,
        PyTypedFile,
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
    "StubGenerationWorkflow",
    "PythonVersionFile",
    "PyTypedFile",
    "AnyFile",
    "Dependency",
]
