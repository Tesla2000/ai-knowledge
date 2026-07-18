from enum import StrEnum
from enum import auto


class SpellSaveDcModifierType(StrEnum):
    PROFICIENCY_BONUS = auto()
    SPELLCASTING_ABILITY = auto()
    FLAT_BONUS = auto()
