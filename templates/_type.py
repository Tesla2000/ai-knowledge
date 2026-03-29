from enum import auto
from enum import StrEnum


class TemplateType(StrEnum):
    PACKAGE = auto()
    NULL = auto()
    CLI_PACKAGE = auto()
