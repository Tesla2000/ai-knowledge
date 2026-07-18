from dnd.character.actions.damage_resistance_modifier._base import (
    _DamageResistanceModifier as DamageResistanceModifier,
)
from dnd.character.actions.damage_resistance_modifier._rage import (
    _RageDamageResistanceModifier as RageDamageResistanceModifier,
)
from dnd.character.actions.damage_resistance_modifier._type import (
    DamageResistanceModifierType,
)

AnyDamageResistanceModifier = RageDamageResistanceModifier

__all__ = [
    "AnyDamageResistanceModifier",
    "DamageResistanceModifier",
    "DamageResistanceModifierType",
    "RageDamageResistanceModifier",
]
