from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict
from typing import Self

if TYPE_CHECKING:
    from dnd.fight._combat_event import AnyCombatEvent
    from dnd.fight.battlemap import Battlemap
    from dnd.fight.fight_character import FightCharacter


class _AdvantageModifier(BaseModel, ABC):
    model_config = ConfigDict(frozen=True)

    @abstractmethod
    def apply(
        self,
        battlemap: Battlemap,
        attacker: FightCharacter,
        defender: FightCharacter,
    ) -> bool: ...

    def on_event(
        self, event: AnyCombatEvent
    ) -> tuple[Self | None, tuple[AnyCombatEvent, ...]]:
        return self, ()


class _GrantsAdvantageModifier(BaseModel, ABC):
    """Placed on a defender; causes all attackers to gain advantage against them."""
    model_config = ConfigDict(frozen=True)

    @abstractmethod
    def apply(
        self,
        battlemap: Battlemap,
        attacker: FightCharacter,
        defender: FightCharacter,
    ) -> bool: ...

    def on_event(
        self, event: AnyCombatEvent
    ) -> tuple[Self, tuple[AnyCombatEvent, ...]]:
        return self, ()


class _DisadvantageModifier(BaseModel, ABC):
    model_config = ConfigDict(frozen=True)

    @abstractmethod
    def apply(
        self,
        battlemap: Battlemap,
        attacker: FightCharacter,
        defender: FightCharacter,
    ) -> bool: ...

    def on_event(
        self, event: AnyCombatEvent
    ) -> tuple[Self | None, tuple[AnyCombatEvent, ...]]:
        return self, ()
