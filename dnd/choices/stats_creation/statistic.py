from __future__ import annotations

from enum import auto
from enum import Enum
from enum import StrEnum


class Statistic(StrEnum):
    STRENGTH = auto()
    DEXTERITY = auto()
    CONSTITUTION = auto()
    INTELLIGENCE = auto()
    WISDOM = auto()
    CHARISMA = auto()


class StatisticAndAny(str, Enum):
    STRENGTH = "strength"
    DEXTERITY = "dexterity"
    CONSTITUTION = "constitution"
    INTELLIGENCE = "intelligence"
    WISDOM = "wisdom"
    CHARISMA = "charisma"
    ANY_OF_YOUR_CHOICE = "any of your choice"
