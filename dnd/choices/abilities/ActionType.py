from __future__ import annotations

from enum import Enum


class ActionType(str, Enum):
    ACTION = "action"
    BONUS_ACTION = "bonus_action"
    REACTION = "reaction"
    FREE_ACTION = "free_action"
    PASSIVE = "passive"
