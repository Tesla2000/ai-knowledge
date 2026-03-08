from enum import StrEnum, auto


class FileTypes(StrEnum):
    LICENSE = auto()
    PYPROJECT_TOML = auto()
    TEST = auto()
    VERSION_PATCH_WORKFLOW = auto()
    TESTS_WORKFLOW = auto()
    README = auto()
    PRE_COMMIT_CONFIG = auto()
    SETUP_SCRIPT = auto()
    INIT_PY = auto()
