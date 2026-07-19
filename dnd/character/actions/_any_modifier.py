from typing import Annotated, Union

from pydantic import Field

from dnd.character.actions.advantage_modifier import (
    RecklessAdvantageModifier,
    RecklessGrantsAdvantageModifier,
)
from dnd.character.actions.attack_bonus_modifier import RageAttackBonusModifier
from dnd.character.actions.conditional_immunity_modifier import (
    MindlessRageConditionalImmunityModifier,
)
from dnd.character.actions.damage_resistance_modifier import (
    RageDamageResistanceModifier,
)

AnyModifier = Annotated[
    Union[
        RageAttackBonusModifier,
        RecklessAdvantageModifier,
        RecklessGrantsAdvantageModifier,
        RageDamageResistanceModifier,
        MindlessRageConditionalImmunityModifier,
    ],
    Field(discriminator="type"),
]

__all__ = ["AnyModifier"]
