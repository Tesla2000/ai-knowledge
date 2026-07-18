from __future__ import annotations

from typing import Literal

from dnd.character._ability_name import AbilityName
from dnd.character.actions._melee_attack import _MeleeAttack
from dnd.choices.equipment_creation.weapons import HitDieSize


class AttackWithBattleaxe(_MeleeAttack):
    name: Literal[AbilityName.ATTACK_WITH_BATTLEAXE] = AbilityName.ATTACK_WITH_BATTLEAXE

    @classmethod
    def _damage_die(cls) -> HitDieSize:
        return HitDieSize.EIGHT

    @classmethod
    def _ability(cls) -> AbilityName:
        return AbilityName.ATTACK_WITH_BATTLEAXE
