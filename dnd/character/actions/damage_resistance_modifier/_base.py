from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Self

from pydantic import BaseModel, ConfigDict

from dnd.character.actions._damage_type import DamageType

if TYPE_CHECKING:
    from dnd.fight._combat_event import AnyCombatEvent


class _DamageResistanceModifier(BaseModel, ABC):
    model_config = ConfigDict(frozen=True)

    @abstractmethod
    def get_resistances(self) -> frozenset[DamageType]: ...

    def on_event(
        self, event: AnyCombatEvent
    ) -> tuple[Self | None, tuple[AnyCombatEvent, ...]]:
        return self, ()
