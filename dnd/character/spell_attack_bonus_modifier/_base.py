from abc import ABC
from abc import abstractmethod

from pydantic import BaseModel
from pydantic import ConfigDict

from dnd.character._spell_modifier_context import SpellModifierContext


class _SpellAttackBonusModifier(BaseModel, ABC):
    model_config = ConfigDict(frozen=True)

    @abstractmethod
    def apply(self, context: SpellModifierContext) -> int: ...
