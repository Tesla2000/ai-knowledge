from __future__ import annotations

from random import randint
from typing import TYPE_CHECKING, Literal, Protocol, Self, runtime_checkable

from pydantic import InstanceOf

from dnd.character._ability_name import AbilityName
from dnd.character.actions._base_action import Action
from dnd.fight.fight_character import FightCharacter, SpellcasterFightCharacter

if TYPE_CHECKING:
    from dnd.fight.battlemap import Battlemap


@runtime_checkable
class _ChromaticOrbPerformer(Protocol):
    def cast_chromatic_orb(self, battlemap: Battlemap) -> Battlemap: ...


class CastChromaticOrb(Action):
    name: Literal[AbilityName.CHROMATIC_ORB] = AbilityName.CHROMATIC_ORB
    range_tails: Literal[18] = 18
    target_position: tuple[int, int]
    performer: InstanceOf[_ChromaticOrbPerformer]

    @classmethod
    def create(cls, fighter: FightCharacter, battlemap: Battlemap) -> tuple[Self, ...]:
        if not isinstance(fighter, SpellcasterFightCharacter):
            return ()
        if not fighter.has_action:
            return ()
        if fighter.remaining_spell_slots.level_1 == 0:
            return ()
        if AbilityName.CHROMATIC_ORB not in fighter.character.actions:
            return ()

        spell_attack_bonus = sum(
            m.apply(fighter.character)
            for m in fighter.character.spell_attack_bonus_modifiers
        )

        class _Performer:
            def __init__(self, target_pos: tuple[int, int]) -> None:
                self._target_pos = target_pos
                self._spell_attack_bonus = spell_attack_bonus

            def cast_chromatic_orb(self, bm: Battlemap) -> Battlemap:
                result = bm.replace_combatant(
                    fighter.position, fighter.spend_action().spend_level_1_slot()
                )
                target = next(
                    (c for c in result.combatants if c.position == self._target_pos),
                    None,
                )
                if not isinstance(target, FightCharacter):
                    return result
                roll = randint(1, 20) + self._spell_attack_bonus
                if roll < target.ac:
                    return result
                damage = sum(randint(1, 8) for _ in range(3))
                return result.replace_combatant(
                    self._target_pos, target.take_damage(damage)
                )

        results: list[Self] = []
        for combatant in battlemap.combatants:
            if combatant.position == fighter.position:
                continue
            results.append(
                cls(
                    target_position=combatant.position,
                    performer=_Performer(combatant.position),
                )
            )
        return tuple(results)

    def perform(self, battlemap: Battlemap) -> Battlemap:
        return self.performer.cast_chromatic_orb(battlemap)
