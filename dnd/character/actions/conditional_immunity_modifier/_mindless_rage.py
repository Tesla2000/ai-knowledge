from __future__ import annotations

from typing import Literal, Self

from uuid_string import UUIDString

from dnd.character.actions.conditional_immunity_modifier._base import (
    _ConditionalImmunityModifier,
)
from dnd.character.actions.conditional_immunity_modifier._type import (
    ConditionalImmunityModifierType,
)
from dnd._combat_event import AnyCombatEvent, RageEndsEvent
from dnd.fight._condition import Condition


class _MindlessRageConditionalImmunityModifier(_ConditionalImmunityModifier):
    type: Literal[ConditionalImmunityModifierType.MINDLESS_RAGE] = (
        ConditionalImmunityModifierType.MINDLESS_RAGE
    )
    owner_id: UUIDString

    def get_immunities(self) -> frozenset[Condition]:
        return frozenset({Condition.CHARMED, Condition.FRIGHTENED})

    def on_event(
        self, event: AnyCombatEvent
    ) -> tuple[Self | None, tuple[AnyCombatEvent, ...]]:
        match event:
            case RageEndsEvent() if event.target_id == self.owner_id:
                return None, ()
            case _:
                return self, ()
