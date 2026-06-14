from __future__ import annotations

from enum import StrEnum, auto


class ActionType(StrEnum):
    ACTION = auto()
    BONUS_ACTION = auto()
    REACTION = auto()
    FREE_ACTION = auto()
    PASSIVE = auto()
