from __future__ import annotations

from enum import auto
from enum import StrEnum


class Level(StrEnum):
    COMMON = auto()
    UNCOMMON = auto()
    RARE = auto()
    VERY_RARE = auto()
    LEGENDARY = auto()
    ARTIFACT = auto()
    UNIQUE = auto()
    MISTERY = auto()
