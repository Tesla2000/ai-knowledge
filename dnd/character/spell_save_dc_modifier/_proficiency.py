from typing import Literal

from dnd.character._spell_modifier_context import SpellModifierContext
from dnd.character.spell_save_dc_modifier._base import _SpellSaveDcModifier
from dnd.character.spell_save_dc_modifier._type import SpellSaveDcModifierType


class ProficiencyBonus(_SpellSaveDcModifier):
    type: Literal[SpellSaveDcModifierType.PROFICIENCY_BONUS] = (
        SpellSaveDcModifierType.PROFICIENCY_BONUS
    )

    def apply(self, context: SpellModifierContext) -> int:
        return context.proficiency_bonus
