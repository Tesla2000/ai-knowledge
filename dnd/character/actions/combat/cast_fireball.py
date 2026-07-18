from __future__ import annotations

from random import randint
from typing import TYPE_CHECKING, Literal, Protocol, Self, runtime_checkable

from pydantic import InstanceOf

from dnd.character._ability_name import AbilityName
from dnd.character.actions._base_action import Action
from dnd.choices.stats_creation.statistic import Statistic
from dnd.fight.fight_character import FightCharacter, SpellcasterFightCharacter

if TYPE_CHECKING:
    from dnd.fight.battlemap import Battlemap


@runtime_checkable
class _FireballPerformer(Protocol):
    def cast_fireball(self, battlemap: Battlemap) -> Battlemap: ...


class CastFireball(Action):
    name: Literal[AbilityName.FIREBALL] = AbilityName.FIREBALL
    range_tails: Literal[30] = 30
    radius_tails: Literal[4] = 4
    center_position: tuple[int, int]
    performer: InstanceOf[_FireballPerformer]

    @classmethod
    def create(cls, fighter: FightCharacter, battlemap: Battlemap) -> tuple[Self, ...]:
        if not isinstance(fighter, SpellcasterFightCharacter):
            return ()
        if not fighter.has_action:
            return ()
        if fighter.remaining_spell_slots.level_3 == 0:
            return ()
        if AbilityName.FIREBALL not in fighter.character.actions:
            return ()

        spell_save_dc = 8 + sum(
            m.apply(fighter.character)
            for m in fighter.character.spell_save_dc_modifiers
        )
        center = fighter.position

        class _Performer:
            def __init__(self, target_pos: tuple[int, int]) -> None:
                self._center = target_pos
                self._spell_save_dc = spell_save_dc

            def cast_fireball(self, bm: Battlemap) -> Battlemap:
                damage = sum(randint(1, 6) for _ in range(8))
                cx, cy = self._center
                result = bm.replace_combatant(
                    fighter.position, fighter.spend_action().spend_level_3_slot()
                )
                for combatant in bm.combatants:
                    tx, ty = combatant.position
                    if max(abs(tx - cx), abs(ty - cy)) > 4:
                        continue
                    roll = (
                        randint(1, 20)
                        + combatant.character.saving_throw_modifiers[
                            Statistic.DEXTERITY
                        ]
                    )
                    hit_damage = damage if roll < self._spell_save_dc else damage // 2
                    current = next(
                        c for c in result.combatants if c.position == combatant.position
                    )
                    result = result.replace_combatant(
                        combatant.position, current.take_damage(hit_damage)
                    )
                return result

        results: list[Self] = []
        for combatant in battlemap.combatants:
            if combatant.position == center:
                continue
            results.append(
                cls(
                    center_position=combatant.position,
                    performer=_Performer(combatant.position),
                )
            )
        return tuple(results)

    def perform(self, battlemap: Battlemap) -> Battlemap:
        return self.performer.cast_fireball(battlemap)
