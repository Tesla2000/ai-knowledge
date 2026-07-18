from typing import Literal

from dnd.character._spell_modifier_context import SpellModifierContext
from dnd.character.spell_save_dc_modifier._base import _SpellSaveDcModifier
from dnd.character.spell_save_dc_modifier._type import SpellSaveDcModifierType


class FlatSpellSaveDcBonus(_SpellSaveDcModifier):
    type: Literal[SpellSaveDcModifierType.FLAT_BONUS] = (
        SpellSaveDcModifierType.FLAT_BONUS
    )
    bonus: int

    def apply(self, context: SpellModifierContext) -> int:
        return self.bonus
