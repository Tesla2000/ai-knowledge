from typing import Literal
from typing import assert_never

from dnd.character._spell_modifier_context import SpellModifierContext
from dnd.character.spell_save_dc_modifier._base import _SpellSaveDcModifier
from dnd.character.spell_save_dc_modifier._type import SpellSaveDcModifierType
from dnd.choices.stats_creation.statistic import Statistic


class SpellcastingAbility(_SpellSaveDcModifier):
    type: Literal[SpellSaveDcModifierType.SPELLCASTING_ABILITY] = (
        SpellSaveDcModifierType.SPELLCASTING_ABILITY
    )
    statistic: Statistic

    def apply(self, context: SpellModifierContext) -> int:
        match self.statistic:
            case Statistic.STRENGTH:
                score = context.stats.strength
            case Statistic.DEXTERITY:
                score = context.stats.dexterity
            case Statistic.CONSTITUTION:
                score = context.stats.constitution
            case Statistic.INTELLIGENCE:
                score = context.stats.intelligence
            case Statistic.WISDOM:
                score = context.stats.wisdom
            case Statistic.CHARISMA:
                score = context.stats.charisma
            case _:
                assert_never(self.statistic)
        return score // 2 - 5
