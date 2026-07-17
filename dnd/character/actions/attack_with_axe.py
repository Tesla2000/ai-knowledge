from __future__ import annotations

from random import randint
from typing import TYPE_CHECKING, Literal, Protocol, runtime_checkable

from pydantic import InstanceOf
from typing import Self

from dnd.character.actions._ability_name import AbilityName
from dnd.character.actions._base_action import Action
from dnd.choices.abilities.action import AttackAction

if TYPE_CHECKING:
    from dnd.fight.battlemap import Battlemap
    from dnd.fight.fight_character import FightCharacter


@runtime_checkable
class _AttackWithAxePerformer(Protocol):
    def attack_with_axe(self, battlemap: Battlemap) -> Battlemap: ...


class AttackWithAxe(Action):
    name: Literal[AbilityName.ATTACK_WITH_AXE] = AbilityName.ATTACK_WITH_AXE
    range_tails: Literal[1] = 1
    target_position: tuple[int, int]
    performer: InstanceOf[_AttackWithAxePerformer]

    @classmethod
    def create(cls, fighter: FightCharacter, battlemap: Battlemap) -> tuple[Self, ...]:
        class _Performer:
            def __init__(self, target_pos: tuple[int, int]) -> None:
                self._target_pos = target_pos

            def attack_with_axe(self, bm: Battlemap) -> Battlemap:
                roll1 = randint(1, 20)
                roll2 = randint(1, 20)
                _ = (roll1, roll2, fighter.attack_bonus, self._target_pos)
                return bm.replace_combatant(fighter.position, fighter.spend_action())

        attack_action = next(
            (
                a
                for a in fighter.character.actions
                if isinstance(a, AttackAction) and a.range_tails == 1
            ),
            None,
        )
        if not fighter.has_action or attack_action is None:
            return ()
        fx, fy = fighter.position
        results: list[Self] = []
        for combatant in battlemap.combatants:
            tx, ty = combatant.position
            if combatant.position == fighter.position:
                continue
            if max(abs(tx - fx), abs(ty - fy)) > 1:
                continue
            results.append(
                cls(
                    target_position=combatant.position,
                    performer=_Performer(combatant.position),
                )
            )
        return tuple(results)

    def perform(self, battlemap: Battlemap) -> Battlemap:
        return self.performer.attack_with_axe(battlemap)
