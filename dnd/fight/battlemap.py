from __future__ import annotations

from typing import ClassVar

from pydantic import BaseModel, ConfigDict

from uuid_string import UUIDString

from dnd.fight._combat_event import AnyCombatEvent
from dnd.fight.fight_character import AnyActiveCombatant, FightCharacter


class Battlemap(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    combatants: tuple[AnyActiveCombatant, ...]
    event_log: tuple[AnyCombatEvent, ...] = ()

    def replace_combatant(
        self, position: tuple[int, int], updated: AnyActiveCombatant
    ) -> Battlemap:
        return self.model_copy(
            update={
                "combatants": tuple(
                    updated if c.position == position else c for c in self.combatants
                )
            }
        )

    def find_fight_character(self, id: UUIDString) -> FightCharacter | None:
        return next(
            (c for c in self.combatants if isinstance(c, FightCharacter) and c.id == id),
            None,
        )

    def emit(self, event: AnyCombatEvent) -> Battlemap:
        new_combatants: list[AnyActiveCombatant] = []
        pending: list[AnyCombatEvent] = []
        for combatant in self.combatants:
            updated, emitted = combatant.on_event(event)
            new_combatants.append(updated)
            pending.extend(emitted)
        result = self.model_copy(
            update={
                "combatants": tuple(new_combatants),
                "event_log": self.event_log + (event,),
            }
        )
        for next_event in pending:
            result = result.emit(next_event)
        return result
