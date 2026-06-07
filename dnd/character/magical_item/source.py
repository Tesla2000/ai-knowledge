from __future__ import annotations

from enum import auto
from enum import StrEnum


class Source(StrEnum):
    DMG = auto()  # Dungeon Master's Guide
    PHB = auto()  # Player's Handbook
    E_RLW = auto()
    XGE = auto()
    WGTE = auto()
    SCC = auto()
    EGW = auto()
    WDDM = auto()
    CR_CN = auto()
    HOMEBREW = auto()
