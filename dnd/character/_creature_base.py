from typing import ClassVar

from pydantic import BaseModel, ConfigDict, Field, NonNegativeInt, PositiveInt

from dnd.character.spell_attack_bonus_modifier import AnySpellAttackBonusModifier
from dnd.character.spell_save_dc_modifier import AnySpellSaveDcModifier
from dnd.character.stats import Stats
from dnd.choices.stats_creation.statistic import Statistic


class _CreatureBase(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    name: str
    stats: Stats
    speed: PositiveInt
    dark_vision_range: NonNegativeInt
    ac_bonus: NonNegativeInt = Field(0, exclude=True)
    spell_save_dc_modifiers: tuple[AnySpellSaveDcModifier, ...] = Field(default=())
    spell_attack_bonus_modifiers: tuple[AnySpellAttackBonusModifier, ...] = Field(
        default=()
    )
    saving_throw_bonuses: Stats = Field(
        default=Stats(
            strength=0,
            dexterity=0,
            constitution=0,
            intelligence=0,
            wisdom=0,
            charisma=0,
        ),
        exclude=True,
    )
    stats_cup: Stats = Field(
        default=Stats(
            strength=20,
            dexterity=20,
            constitution=20,
            intelligence=20,
            wisdom=20,
            charisma=20,
        ),
        exclude=True,
    )
    initiative_bonus: int = 0
    saving_throw_proficiencies: tuple[Statistic, ...]
    other_active_abilities: tuple[str, ...]
