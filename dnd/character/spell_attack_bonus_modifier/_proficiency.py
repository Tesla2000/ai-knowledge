from typing import Literal

from dnd.character._spell_modifier_context import SpellModifierContext
from dnd.character.spell_attack_bonus_modifier._base import _SpellAttackBonusModifier
from dnd.character.spell_attack_bonus_modifier._type import SpellAttackBonusModifierType


class ProficiencyBonus(_SpellAttackBonusModifier):
    type: Literal[SpellAttackBonusModifierType.PROFICIENCY_BONUS] = (
        SpellAttackBonusModifierType.PROFICIENCY_BONUS
    )

    def apply(self, context: SpellModifierContext) -> int:
        return context.proficiency_bonus
