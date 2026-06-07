from __future__ import annotations

from enum import auto
from enum import StrEnum

from frozendict import frozendict


class CasterType(StrEnum):
    """Types of spellcasting progression."""

    FULL = auto()
    HALF = auto()
    ELDRITCH_KNIGHT = auto()
    WARLOCK = auto()
    NONE = auto()


MAX_SPELL_LEVELS = frozendict(
    {
        CasterType.FULL: (
            1,
            1,
            2,
            2,
            3,
            3,
            4,
            4,
            5,
            5,
            6,
            6,
            7,
            7,
            8,
            8,
            9,
            9,
            9,
            9,
        ),
        CasterType.HALF: (
            0,
            1,
            1,
            1,
            2,
            2,
            2,
            2,
            3,
            3,
            3,
            3,
            4,
            4,
            4,
            4,
            5,
            5,
            5,
            5,
        ),
        CasterType.WARLOCK: (
            1,  # 1st level
            1,  # 2nd level
            2,  # 3rd level
            2,  # 4th level
            3,  # 5th level
            3,  # 6th level
            4,  # 7th level
            4,  # 8th level
            5,  # 9th level
            5,  # 10th level
            5,  # 11th level
            5,  # 12th level
            5,  # 13th level
            5,  # 14th level
            5,  # 15th level
            5,  # 16th level
            5,  # 17th level
            5,  # 18th level
            5,  # 19th level
            5,  # 20th level
        ),
        CasterType.ELDRITCH_KNIGHT: (
            0,  # 1st level
            0,  # 2nd level
            1,  # 3rd level
            1,  # 4th level
            1,  # 5th level
            1,  # 6th level
            2,  # 7th level
            2,  # 8th level
            2,  # 9th level
            3,  # 10th level
            3,  # 11th level
            3,  # 12th level
            3,  # 13th level
            3,  # 14th level
            3,  # 15th level
            4,  # 16th level
            4,  # 17th level
            4,  # 18th level
            4,  # 19th level
            4,  # 20th level
        ),
        CasterType.NONE: tuple(0 for _ in range(20)),
    }
)
if not all(map(MAX_SPELL_LEVELS.__contains__, CasterType)):
    raise ValueError(
        f"Not all Caster types defined in {','.join(map(str, MAX_SPELL_LEVELS.keys()))}"
    )
