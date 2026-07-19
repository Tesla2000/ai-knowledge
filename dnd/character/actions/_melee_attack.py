from __future__ import annotations

from abc import abstractmethod
from random import randint
from typing import TYPE_CHECKING, ClassVar, Generic, Literal, Self
from uuid import uuid4

from pydantic import BaseModel, ConfigDict
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
from dnd.choices.equipment_creation.weapons import HitDieSize, WeaponName
from dnd.fight._combatant_slot import SlotT
from dnd.fight.fight_character import FightCharacter

if TYPE_CHECKING:
    from dnd.fight.battlemap import Battlemap


class _MeleeAttackExecutor(BaseModel, Generic[SlotT]):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)
    actor_slot: SlotT
    target_slot: SlotT
    die: HitDieSize
    is_oa: bool = False

    def attack(self, bm: Battlemap[SlotT]) -> Battlemap[SlotT]:
        match bm.get_combatant(self.actor_slot):
            case FightCharacter() as fighter:
                pass
            case _:
                return bm

        if self.is_oa:
            bm = bm.replace_combatant(self.actor_slot, fighter.spend_reaction())
        else:
            bm = bm.replace_combatant(self.actor_slot, fighter.spend_attack())

        match bm.get_combatant(self.target_slot):
            case FightCharacter() as target:
                pass
            case _:
                return bm

        attack_id = UUIDString(str(uuid4()))

        bm = bm.emit(
            CreatureTargetedEvent(
                attacker_id=fighter.id,
                defender_id=target.id,
                attack_id=attack_id,
            )
        )

        match bm.get_combatant(self.actor_slot):
            case FightCharacter() as fighter:
                pass
            case _:
                return bm

        match bm.get_combatant(self.target_slot):
            case FightCharacter() as target:
                pass
            case _:
                return bm

        use_advantage = any(
            isinstance(m, AdvantageModifier) and m.apply(fighter, target)
            for m in fighter.modifiers
        ) or any(
            isinstance(m, GrantsAdvantageModifier) and m.apply(fighter, target)
            for m in target.modifiers
        )
        use_disadvantage = any(
            isinstance(m, DisadvantageModifier) and m.apply(fighter, target)
            for m in fighter.modifiers
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
            m.apply(fighter, target)
            for m in fighter.modifiers
            if isinstance(m, AttackBonusModifier)
        )

        bm = bm.emit(
            CreatureAttackedEvent(
                attacker_id=fighter.id,
                defender_id=target.id,
                roll=roll,
                total_bonus=total_bonus,
                is_crit=is_crit,
                attack_id=attack_id,
            )
        )

        match bm.get_combatant(self.target_slot):
            case FightCharacter() as target:
                pass
            case _:
                return bm

        if roll + total_bonus >= target.ac:
            damage = randint(1, int(self.die))
            match bm.get_combatant(self.actor_slot):
                case FightCharacter() as fighter:
                    pass
                case _:
                    return bm
            if is_crit:
                damage += sum(
                    randint(1, int(self.die))
                    for _ in range(fighter.brutal_critical_dice)
                )

            bm = bm.emit(
                MeleeDamageEvent(
                    attacker_id=fighter.id,
                    defender_id=target.id,
                    damage=damage,
                    is_crit=is_crit,
                    attack_id=attack_id,
                )
            )

            match bm.get_combatant(self.target_slot):
                case FightCharacter() as target:
                    bm = bm.replace_combatant(
                        self.target_slot, target.take_damage(damage)
                    )
                case _:
                    pass

        return bm


class _MeleeAttack(Action[SlotT], Generic[SlotT]):
    range_tails: Literal[1] = 1
    actor_slot: SlotT
    executor: _MeleeAttackExecutor[SlotT]

    @classmethod
    @abstractmethod
    def _damage_die(cls) -> HitDieSize: ...

    @classmethod
    @abstractmethod
    def _ability(cls) -> AbilityName: ...

    @classmethod
    @abstractmethod
    def _weapon(cls) -> WeaponName: ...

    @classmethod
    @abstractmethod
    def _two_handed(cls) -> bool: ...

    @classmethod
    def create(
        cls, actor_slot: SlotT, fighter: FightCharacter, battlemap: Battlemap[SlotT]
    ) -> tuple[Self, ...]:
        if (
            fighter.attacks_remaining <= 0
            or cls._ability() not in fighter.character.actions
        ):
            return ()
        weapon = cls._weapon()
        if cls._two_handed():
            if fighter.main_hand != weapon or fighter.off_hand != weapon:
                return ()
        else:
            if fighter.main_hand != weapon and fighter.off_hand != weapon:
                return ()
        fx, fy = fighter.position
        die = cls._damage_die()
        results: list[Self] = []
        for target_slot in battlemap.all_slots():
            match battlemap.get_combatant(target_slot):
                case FightCharacter() as target if target.position != fighter.position:
                    tx, ty = target.position
                    if max(abs(tx - fx), abs(ty - fy)) <= 1:
                        results.append(
                            cls(
                                name=cls._ability(),
                                actor_slot=actor_slot,
                                executor=_MeleeAttackExecutor(
                                    actor_slot=actor_slot,
                                    target_slot=target_slot,
                                    die=die,
                                ),
                            )
                        )
                case _:
                    pass
        return tuple(results)

    @classmethod
    def create_oa(
        cls,
        actor_slot: SlotT,
        attacker: FightCharacter,
        target_slot: SlotT,
        battlemap: Battlemap[SlotT],
    ) -> tuple[Self, ...]:
        if cls._ability() not in attacker.character.actions:
            return ()
        if not attacker.has_reaction:
            return ()
        die = cls._damage_die()
        return (
            cls(
                name=cls._ability(),
                actor_slot=actor_slot,
                executor=_MeleeAttackExecutor(
                    actor_slot=actor_slot,
                    target_slot=target_slot,
                    die=die,
                    is_oa=True,
                ),
            ),
        )

    def perform(self, battlemap: Battlemap[SlotT]) -> Battlemap[SlotT]:
        return self.executor.attack(battlemap)
