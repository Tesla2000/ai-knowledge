from typing import Literal

from dnd.character._spell_modifier_context import SpellModifierContext
from dnd.character.spell_attack_bonus_modifier._base import _SpellAttackBonusModifier
from dnd.character.spell_attack_bonus_modifier._type import SpellAttackBonusModifierType


class FlatSpellAttackBonus(_SpellAttackBonusModifier):
    type: Literal[SpellAttackBonusModifierType.FLAT_BONUS] = (
        SpellAttackBonusModifierType.FLAT_BONUS
    )
    bonus: int

    def apply(self, context: SpellModifierContext) -> int:
        return self.bonus
