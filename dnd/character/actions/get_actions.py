from __future__ import annotations

from enum import IntEnum

from dnd.character._ability_name import AbilityName
from dnd.character.actions.combat import (
    AnyCombatAction,
    AttackWithAxe,
    AttackWithBattleaxe,
    AttackWithGreataxe,
    AttackWithHandaxe,
    CastChromaticOrb,
    CastFireball,
    DrawItem,
    DropItem,
    Pass,
    UseRage,
    UseRecklessAttack,
)
from dnd.fight.battlemap import Battlemap
from dnd.fight.fight_character import FightCharacter


def get_actions[T: IntEnum](
    actor_slot: T,
    fighter: FightCharacter,
    battlemap: Battlemap[T],
) -> tuple[tuple[AnyCombatAction[T], ...], ...]:
    candidates: list[tuple[AnyCombatAction[T], ...]] = []
    for action_name in fighter.character.actions:
        match action_name:
            case AbilityName.ATTACK_WITH_AXE:
                axe_options = AttackWithAxe.create(actor_slot, fighter, battlemap)
                if axe_options:
                    candidates.append(axe_options)
            case AbilityName.ATTACK_WITH_BATTLEAXE:
                battleaxe_options = AttackWithBattleaxe.create(
                    actor_slot, fighter, battlemap
                )
                if battleaxe_options:
                    candidates.append(battleaxe_options)
            case AbilityName.ATTACK_WITH_GREATAXE:
                greataxe_options = AttackWithGreataxe.create(
                    actor_slot, fighter, battlemap
                )
                if greataxe_options:
                    candidates.append(greataxe_options)
            case AbilityName.ATTACK_WITH_HANDAXE:
                handaxe_options = AttackWithHandaxe.create(
                    actor_slot, fighter, battlemap
                )
                if handaxe_options:
                    candidates.append(handaxe_options)
            case AbilityName.CHROMATIC_ORB:
                orb_options = CastChromaticOrb.create(actor_slot, fighter, battlemap)
                if orb_options:
                    candidates.append(orb_options)
            case AbilityName.FIREBALL:
                fireball_options = CastFireball.create(actor_slot, fighter, battlemap)
                if fireball_options:
                    candidates.append(fireball_options)
            case AbilityName.RAGE:
                rage_options = UseRage.create(actor_slot, fighter, battlemap)
                if rage_options:
                    candidates.append(rage_options)
            case AbilityName.RECKLESS_ATTACK:
                reckless_options = UseRecklessAttack.create(
                    actor_slot, fighter, battlemap
                )
                if reckless_options:
                    candidates.append(reckless_options)
            case _:
                pass
    pass_options = Pass.create(actor_slot, fighter, battlemap)
    if pass_options:
        candidates.append(pass_options)
    drop_options = DropItem.create(actor_slot, fighter, battlemap)
    if drop_options:
        candidates.append(drop_options)
    draw_options = DrawItem.create(actor_slot, fighter, battlemap)
    if draw_options:
        candidates.append(draw_options)
    return tuple(candidates)
