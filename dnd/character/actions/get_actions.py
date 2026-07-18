from __future__ import annotations

from typing import TYPE_CHECKING

from dnd.character._ability_name import AbilityName
from dnd.character.actions.combat import (
    AnyCombatAction,
    AttackWithAxe,
    AttackWithBattleaxe,
    AttackWithGreataxe,
    AttackWithHandaxe,
    CastChromaticOrb,
    CastFireball,
    UseRage,
    UseRecklessAttack,
)
from dnd.fight.fight_character import FightCharacter

if TYPE_CHECKING:
    from dnd.fight.battlemap import Battlemap


def get_actions(
    fighter: FightCharacter, battlemap: Battlemap
) -> tuple[tuple[AnyCombatAction, ...], ...]:
    candidates: list[tuple[AnyCombatAction, ...]] = []
    for action_name in fighter.character.actions:
        match action_name:
            case AbilityName.ATTACK_WITH_AXE:
                options = AttackWithAxe.create(fighter, battlemap)
                if options:
                    candidates.append(options)
            case AbilityName.ATTACK_WITH_BATTLEAXE:
                options = AttackWithBattleaxe.create(fighter, battlemap)
                if options:
                    candidates.append(options)
            case AbilityName.ATTACK_WITH_GREATAXE:
                options = AttackWithGreataxe.create(fighter, battlemap)
                if options:
                    candidates.append(options)
            case AbilityName.ATTACK_WITH_HANDAXE:
                options = AttackWithHandaxe.create(fighter, battlemap)
                if options:
                    candidates.append(options)
            case AbilityName.CHROMATIC_ORB:
                orb_options = CastChromaticOrb.create(fighter, battlemap)
                if orb_options:
                    candidates.append(orb_options)
            case AbilityName.FIREBALL:
                fireball_options = CastFireball.create(fighter, battlemap)
                if fireball_options:
                    candidates.append(fireball_options)
            case AbilityName.RAGE:
                rage_options = UseRage.create(fighter)
                if rage_options:
                    candidates.append(rage_options)
            case AbilityName.RECKLESS_ATTACK:
                reckless_options = UseRecklessAttack.create(fighter)
                if reckless_options:
                    candidates.append(reckless_options)
            case _:
                pass
    return tuple(candidates)
