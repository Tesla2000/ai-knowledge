from __future__ import annotations

from abc import ABC, abstractmethod
from typing import ClassVar, Generic, Self

from pydantic import BaseModel, ConfigDict

from dnd.fight._combat_event import AnyCombatEvent
from dnd.fight._combatant_slot import SlotT
from dnd.fight.fight_character import AnyActiveCombatant


class Battlemap(BaseModel, Generic[SlotT], ABC):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)
    event_log: tuple[AnyCombatEvent, ...] = ()

    @abstractmethod
    def all_slots(self) -> tuple[SlotT, ...]: ...

    @abstractmethod
    def get_combatant(self, slot: SlotT) -> AnyActiveCombatant: ...

    @abstractmethod
    def replace_combatant(self, slot: SlotT, updated: AnyActiveCombatant) -> Self: ...

    def emit(self, event: AnyCombatEvent) -> Self:
        result: Self = self
        pending: list[AnyCombatEvent] = []
        for slot in result.all_slots():
            combatant = result.get_combatant(slot)
            updated, emitted = combatant.on_event(event)
            result = result.replace_combatant(slot, updated)
            pending.extend(emitted)
        result = result.model_copy(update={"event_log": result.event_log + (event,)})
        for next_event in pending:
            result = result.emit(next_event)
        return result
