from enum import StrEnum, auto


class ActionType(StrEnum):
    ACTION = auto()
    BONUS_ACTION = auto()
    REACTION = auto()
    FREE_ACTION = auto()
    PASSIVE = auto()
    SHORT_REST = auto()
    SHORT_OR_LONG_REST = auto()
