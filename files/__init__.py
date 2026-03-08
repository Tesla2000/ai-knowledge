from typing import Annotated, Union

from pydantic import Discriminator

from files.file import File
from files.package_init_py import PackageInitPy
from files.mit_license import MitLicense
from files.package_pyproject_toml import PackagePyprojectToml
from files.pre_commit_config import PreCommitConfig
from files.readme import ReadmeFile
from files.setup_script import SetupScript
from files.test_import_file import TestImportFile
from files.tests_workflow import TestsWorkflow
from files.version_patch_workflow import VersionPatchWorkflow

AnyFile = Annotated[
    Union[
        File,
        PackageInitPy,
        MitLicense,
        PackagePyprojectToml,
        PreCommitConfig,
        ReadmeFile,
        TestImportFile,
        TestsWorkflow,
        SetupScript,
        VersionPatchWorkflow,
    ], Discriminator("type")
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
    "PackageInitPy",
    "AnyFile",
]

