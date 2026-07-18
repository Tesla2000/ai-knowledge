from typing import Annotated
from typing import Union

from pydantic import Field

from dnd.character.spell_save_dc_modifier._base import (
    _SpellSaveDcModifier as SpellSaveDcModifier,
)
from dnd.character.spell_save_dc_modifier._flat_bonus import FlatSpellSaveDcBonus
from dnd.character.spell_save_dc_modifier._proficiency import ProficiencyBonus
from dnd.character.spell_save_dc_modifier._spellcasting_ability import (
    SpellcastingAbility,
)
from dnd.character.spell_save_dc_modifier._type import SpellSaveDcModifierType

AnySpellSaveDcModifier = Annotated[
    Union[ProficiencyBonus, SpellcastingAbility, FlatSpellSaveDcBonus],
    Field(discriminator="type"),
]

__all__ = [
    "AnySpellSaveDcModifier",
    "FlatSpellSaveDcBonus",
    "ProficiencyBonus",
    "SpellSaveDcModifier",
    "SpellSaveDcModifierType",
    "SpellcastingAbility",
]
