from enum import IntEnum
from typing import Union

from dnd.character.actions._base_action import (
    Action,
    BaseAction,
    BonusAction,
    CombatAction,
    FreeAction,
    MovementAction,
)
from dnd.character.actions.combat.attack_with_axe import AttackWithAxe
from dnd.character.actions.combat.attack_with_battleaxe import AttackWithBattleaxe
from dnd.character.actions.combat.attack_with_greataxe import AttackWithGreataxe
from dnd.character.actions.combat.attack_with_handaxe import AttackWithHandaxe
from dnd.character.actions.combat.cast_chromatic_orb import CastChromaticOrb
from dnd.character.actions.combat.cast_fireball import CastFireball
from dnd.character.actions.combat.draw_item import DrawItem
from dnd.character.actions.combat.drop_item import DropItem
from dnd.character.actions.combat.move import Move
from dnd.character.actions.combat.pass_turn import Pass
from dnd.character.actions.combat.use_rage import UseRage
from dnd.character.actions.combat.use_reckless_attack import UseRecklessAttack

type AnyCombatAction[T: IntEnum] = Union[
    AttackWithAxe[T],
    AttackWithBattleaxe[T],
    AttackWithGreataxe[T],
    AttackWithHandaxe[T],
    CastChromaticOrb[T],
    CastFireball[T],
    DrawItem[T],
    DropItem[T],
    Move[T],
    Pass[T],
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
    "DrawItem",
    "DropItem",
    "FreeAction",
    "Move",
    "MovementAction",
    "Pass",
    "UseRage",
    "UseRecklessAttack",
]
