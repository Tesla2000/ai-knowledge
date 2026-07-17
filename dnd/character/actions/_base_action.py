from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, ClassVar

from pydantic import BaseModel, ConfigDict, NonNegativeInt

from dnd.character.actions._ability_name import AbilityName

if TYPE_CHECKING:
    from dnd.fight.battlemap import Battlemap


class BaseAction(BaseModel, ABC):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    name: AbilityName
    range_tails: NonNegativeInt
    radius_tails: NonNegativeInt = 0

    @abstractmethod
    def perform(self, battlemap: Battlemap) -> Battlemap: ...


class CombatAction(BaseAction, ABC):
    pass


class Action(CombatAction, ABC):
    pass


class BonusAction(CombatAction, ABC):
    pass
