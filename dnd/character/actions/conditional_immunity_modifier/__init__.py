from dnd.character.actions.conditional_immunity_modifier._base import (
    _ConditionalImmunityModifier as ConditionalImmunityModifier,
)
from dnd.character.actions.conditional_immunity_modifier._mindless_rage import (
    _MindlessRageConditionalImmunityModifier as MindlessRageConditionalImmunityModifier,
)
from dnd.character.actions.conditional_immunity_modifier._type import (
    ConditionalImmunityModifierType,
)

AnyConditionalImmunityModifier = MindlessRageConditionalImmunityModifier

__all__ = [
    "AnyConditionalImmunityModifier",
    "ConditionalImmunityModifier",
    "ConditionalImmunityModifierType",
    "MindlessRageConditionalImmunityModifier",
]
