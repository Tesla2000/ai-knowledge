from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, ClassVar, Generic

from pydantic import BaseModel, ConfigDict, NonNegativeInt

from dnd.character._ability_name import AbilityName
from dnd.fight._combatant_slot import SlotT

if TYPE_CHECKING:
    from dnd.fight.battlemap import Battlemap


class BaseAction(BaseModel, Generic[SlotT], ABC):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    name: AbilityName
    range_tails: NonNegativeInt
    radius_tails: NonNegativeInt = 0

    @abstractmethod
    def perform(self, battlemap: Battlemap[SlotT]) -> Battlemap[SlotT]: ...


class CombatAction(BaseAction[SlotT], Generic[SlotT], ABC):
    pass


class Action(CombatAction[SlotT], Generic[SlotT], ABC):
    pass


class BonusAction(CombatAction[SlotT], Generic[SlotT], ABC):
    pass


class FreeAction(CombatAction[SlotT], Generic[SlotT], ABC):
    pass


class MovementAction(CombatAction[SlotT], Generic[SlotT], ABC):
    pass
