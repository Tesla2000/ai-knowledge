from dnd.character.actions.attack_bonus_modifier._base import (
    _AttackBonusModifier as AttackBonusModifier,
)
from dnd.character.actions.attack_bonus_modifier._rage import (
    _RageAttackBonusModifier as RageAttackBonusModifier,
)
from dnd.character.actions.attack_bonus_modifier._type import AttackBonusModifierType

AnyAttackBonusModifier = RageAttackBonusModifier

__all__ = [
    "AnyAttackBonusModifier",
    "AttackBonusModifier",
    "AttackBonusModifierType",
    "RageAttackBonusModifier",
]
