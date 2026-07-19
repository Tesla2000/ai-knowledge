from __future__ import annotations

from typing import Literal, Self

from uuid_string import UUIDString

from dnd.character.actions._damage_type import DamageType
from dnd.character.actions.damage_resistance_modifier._base import (
    _DamageResistanceModifier,
)
from dnd.character.actions.damage_resistance_modifier._type import (
    DamageResistanceModifierType,
)
from dnd._combat_event import AnyCombatEvent, RageEndsEvent


class _RageDamageResistanceModifier(_DamageResistanceModifier):
    type: Literal[DamageResistanceModifierType.RAGE] = DamageResistanceModifierType.RAGE
    owner_id: UUIDString

    def get_resistances(self) -> frozenset[DamageType]:
        return frozenset(
            {DamageType.BLUDGEONING, DamageType.PIERCING, DamageType.SLASHING}
        )

    def on_event(
        self, event: AnyCombatEvent
    ) -> tuple[Self | None, tuple[AnyCombatEvent, ...]]:
        match event:
            case RageEndsEvent() if event.target_id == self.owner_id:
                return None, ()
            case _:
                return self, ()
