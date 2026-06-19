from typing import Annotated

from pydantic import Discriminator

from src.files.devcontainer import (
    DevcontainerDockerComposeFile,
    DevcontainerJsonFile,
)
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
    File
    | PackageFile
    | MitLicense
    | Gitignore
    | PackagePyprojectToml
    | PreCommitConfig
    | ReadmeFile
    | TestsWorkflow
    | SetupScript
    | VersionPatchWorkflow
    | PreCommitRunWorkflow
    | PyTypedFile
    | CodeOwnersFile
    | PythonVersionFile
    | DevcontainerJsonFile
    | DevcontainerDockerComposeFile,
    Discriminator("type"),
]

__all__ = [
    "AnyFile",
    "CodeOwnersFile",
    "Dependency",
    "DevcontainerDockerComposeFile",
    "DevcontainerDockerComposeFile",
    "DevcontainerJsonFile",
    "File",
    "Gitignore",
    "MitLicense",
    "PackageFile",
    "PackagePyprojectToml",
    "PreCommitConfig",
    "PreCommitRunWorkflow",
    "PyTypedFile",
    "PythonVersion",
    "PythonVersionFile",
    "ReadmeFile",
    "SetupScript",
    "TestsWorkflow",
    "VersionPatchWorkflow",
]
