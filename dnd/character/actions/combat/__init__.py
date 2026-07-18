from typing import Annotated, Union

from pydantic import Field

from dnd.character.actions._base_action import (
    Action,
    BaseAction,
    BonusAction,
    CombatAction,
    FreeAction,
)
from dnd.character.actions.combat.attack_with_axe import AttackWithAxe
from dnd.character.actions.combat.attack_with_battleaxe import AttackWithBattleaxe
from dnd.character.actions.combat.attack_with_greataxe import AttackWithGreataxe
from dnd.character.actions.combat.attack_with_handaxe import AttackWithHandaxe
from dnd.character.actions.combat.cast_chromatic_orb import CastChromaticOrb
from dnd.character.actions.combat.cast_fireball import CastFireball
from dnd.character.actions.combat.use_rage import UseRage
from dnd.character.actions.combat.use_reckless_attack import UseRecklessAttack

AnyCombatAction = Annotated[
    Union[
        AttackWithAxe,
        AttackWithBattleaxe,
        AttackWithGreataxe,
        AttackWithHandaxe,
        CastChromaticOrb,
        CastFireball,
        UseRage,
        UseRecklessAttack,
    ],
    Field(discriminator="name"),
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
