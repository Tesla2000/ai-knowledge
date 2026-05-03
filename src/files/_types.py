from enum import StrEnum, auto


class FileType(StrEnum):
    FILE = auto()
    LICENSE = auto()
    GITIGNORE = auto()
    PYPROJECT_TOML = auto()
    TEST = auto()
    VERSION_PATCH_WORKFLOW = auto()
    PRE_COMMIT_RUN_WORKFLOW = auto()
    TESTS_WORKFLOW = auto()
    README = auto()
    PRE_COMMIT_CONFIG = auto()
    SETUP_SCRIPT = auto()
    PACKAGE = auto()
    STUB_GENERATION_WORKFLOW = auto()
    PYTHON_VERSION = auto()
    PY_TYPED = auto()
    CODE_OWNERS = auto()
