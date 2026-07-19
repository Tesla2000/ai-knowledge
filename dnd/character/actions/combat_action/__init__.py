from enum import IntEnum
from typing import Union

from dnd.character.actions._base_action import (
    Action,
    BaseAction,
    BonusAction,
    CombatAction,
    FreeAction,
)
from dnd.character.actions.attack_with_battleaxe import AttackWithBattleaxe
from dnd.character.actions.attack_with_greataxe import AttackWithGreataxe
from dnd.character.actions.attack_with_handaxe import AttackWithHandaxe
from dnd.character.actions.cast_chromatic_orb import CastChromaticOrb
from dnd.character.actions.cast_fireball import CastFireball
from dnd.character.actions.combat.attack_with_axe import AttackWithAxe
from dnd.character.actions.combat.use_rage import UseRage
from dnd.character.actions.use_reckless_attack import UseRecklessAttack

type AnyCombatAction[T: IntEnum] = Union[
    AttackWithAxe[T],
    AttackWithBattleaxe[T],
    AttackWithGreataxe[T],
    AttackWithHandaxe[T],
    CastChromaticOrb[T],
    CastFireball[T],
    UseRage[T],
    UseRecklessAttack[T],
]

__all__ = [
    "Action",
    "AnyCombatAction",
    "AttackWithAxe",
    "AttackWithBattleaxe",
    "AttackWithGreataxe",
    "AttackWithHandaxe",
    "BaseAction",
    "BonusAction",
    "CastChromaticOrb",
    "CastFireball",
    "CombatAction",
    "FreeAction",
    "UseRage",
    "UseRecklessAttack",
]
