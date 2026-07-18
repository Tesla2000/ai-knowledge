from __future__ import annotations

from typing import Literal

from dnd.character._ability_name import AbilityName
from dnd.character.actions._melee_attack import _MeleeAttack
from dnd.choices.equipment_creation.weapons import HitDieSize


class AttackWithGreataxe(_MeleeAttack):
    name: Literal[AbilityName.ATTACK_WITH_GREATAXE] = AbilityName.ATTACK_WITH_GREATAXE

    @classmethod
    def _damage_die(cls) -> HitDieSize:
        return HitDieSize.TWELVE

    @classmethod
    def _ability(cls) -> AbilityName:
        return AbilityName.ATTACK_WITH_GREATAXE
