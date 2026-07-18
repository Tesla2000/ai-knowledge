from __future__ import annotations

from abc import abstractmethod
from random import randint
from typing import TYPE_CHECKING, Literal, Protocol, runtime_checkable
from uuid import uuid4

from pydantic import InstanceOf
from typing import Self
from uuid_string import UUIDString

from dnd._combat_event import (
    CreatureAttackedEvent,
    CreatureTargetedEvent,
    MeleeDamageEvent,
)
from dnd.character._ability_name import AbilityName
from dnd.character.actions._base_action import Action
from dnd.character.actions.advantage_modifier import (
    AdvantageModifier,
    DisadvantageModifier,
    GrantsAdvantageModifier,
)
from dnd.character.actions.attack_bonus_modifier import AttackBonusModifier
from dnd.choices.equipment_creation.weapons import HitDieSize
from dnd.fight.fight_character import FightCharacter

if TYPE_CHECKING:
    from dnd.fight.battlemap import Battlemap


@runtime_checkable
class _MeleeAttackPerformer(Protocol):
    def attack(self, battlemap: Battlemap) -> Battlemap: ...


class _MeleeAttack(Action):
    range_tails: Literal[1] = 1
    target_position: tuple[int, int]
    performer: InstanceOf[_MeleeAttackPerformer]

    @classmethod
    @abstractmethod
    def _damage_die(cls) -> HitDieSize: ...

    @classmethod
    @abstractmethod
    def _ability(cls) -> AbilityName: ...

    @classmethod
    def create(cls, fighter: FightCharacter, battlemap: Battlemap) -> tuple[Self, ...]:
        class _Performer:
            def __init__(
                self,
                fighter_id: UUIDString,
                target_id: UUIDString,
                die: HitDieSize,
            ) -> None:
                self._fighter_id = fighter_id
                self._target_id = target_id
                self._die = die

            def attack(self, bm: Battlemap) -> Battlemap:
                current_fighter = bm.find_fight_character(self._fighter_id)
                if current_fighter is None:
                    return bm
                target_opt = bm.find_fight_character(self._target_id)

                bm = bm.replace_combatant(
                    current_fighter.position, current_fighter.spend_attack()
                )

                if target_opt is None:
                    return bm

                attack_id = UUIDString(str(uuid4()))

                bm = bm.emit(
                    CreatureTargetedEvent(
                        attacker_id=self._fighter_id,
                        defender_id=self._target_id,
                        attack_id=attack_id,
                    )
                )

                current_fighter = bm.find_fight_character(self._fighter_id)
                if current_fighter is None:
                    return bm

                target_opt = bm.find_fight_character(self._target_id)
                if target_opt is None:
                    return bm

                use_advantage = any(
                    m.apply(bm, current_fighter, target_opt)
                    for m in current_fighter.modifiers
                    if isinstance(m, AdvantageModifier)
                ) or any(
                    m.apply(bm, current_fighter, target_opt)
                    for m in target_opt.modifiers
                    if isinstance(m, GrantsAdvantageModifier)
                )
                use_disadvantage = any(
                    m.apply(bm, current_fighter, target_opt)
                    for m in current_fighter.modifiers
                    if isinstance(m, DisadvantageModifier)
                )
                roll1 = randint(1, 20)
                roll2 = randint(1, 20) if (use_advantage or use_disadvantage) else roll1
                if use_advantage and not use_disadvantage:
                    roll = max(roll1, roll2)
                elif use_disadvantage and not use_advantage:
                    roll = min(roll1, roll2)
                else:
                    roll = roll1
                is_crit = roll == 20
                total_bonus = sum(
                    m.apply(bm, current_fighter, target_opt)
                    for m in current_fighter.modifiers
                    if isinstance(m, AttackBonusModifier)
                )

                bm = bm.emit(
                    CreatureAttackedEvent(
                        attacker_id=self._fighter_id,
                        defender_id=self._target_id,
                        roll=roll,
                        total_bonus=total_bonus,
                        is_crit=is_crit,
                        attack_id=attack_id,
                    )
                )

                target_opt = bm.find_fight_character(self._target_id)
                if target_opt is None:
                    return bm

                if roll + total_bonus >= target_opt.ac:
                    damage = randint(1, int(self._die))
                    if is_crit:
                        damage += sum(
                            randint(1, int(self._die))
                            for _ in range(current_fighter.brutal_critical_dice)
                        )

                    bm = bm.emit(
                        MeleeDamageEvent(
                            attacker_id=self._fighter_id,
                            defender_id=self._target_id,
                            damage=damage,
                            is_crit=is_crit,
                            attack_id=attack_id,
                        )
                    )

                    target_opt = bm.find_fight_character(self._target_id)
                    if target_opt is not None:
                        bm = bm.replace_combatant(
                            target_opt.position, target_opt.take_damage(damage)
                        )

                return bm

        if (
            fighter.attacks_remaining <= 0
            or cls._ability() not in fighter.character.actions
        ):
            return ()
        fx, fy = fighter.position
        die = cls._damage_die()
        results: list[Self] = []
        for combatant in battlemap.combatants:
            if not isinstance(combatant, FightCharacter):
                continue
            if combatant.position == fighter.position:
                continue
            tx, ty = combatant.position
            if max(abs(tx - fx), abs(ty - fy)) > 1:
                continue
            results.append(
                cls(
                    target_position=combatant.position,
                    performer=_Performer(fighter.id, combatant.id, die),
                )
            )
        return tuple(results)

    def perform(self, battlemap: Battlemap) -> Battlemap:
        return self.performer.attack(battlemap)
