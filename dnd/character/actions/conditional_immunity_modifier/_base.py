from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Self

from pydantic import BaseModel, ConfigDict

from dnd.fight._condition import Condition

if TYPE_CHECKING:
    from dnd.fight._combat_event import AnyCombatEvent


class _ConditionalImmunityModifier(BaseModel, ABC):
    model_config = ConfigDict(frozen=True)

    @abstractmethod
    def get_immunities(self) -> frozenset[Condition]: ...

    def on_event(
        self, event: AnyCombatEvent
    ) -> tuple[Self | None, tuple[AnyCombatEvent, ...]]:
        return self, ()
