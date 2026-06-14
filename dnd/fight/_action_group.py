from random import choice
from typing import ClassVar

from pydantic import BaseModel, ConfigDict

from dnd.fight._attack import _Attack
from dnd.fight._attack_result import _AttackResult
from dnd.fight._saving_throw import _SavingThrow
from dnd.fight._saving_throw_result import _SavingThrowResult

type _Action = _Attack | _SavingThrow


class _Or(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    name: str = ""
    options: tuple[_Action, ...]

    def perform(self) -> _AttackResult | _SavingThrowResult:
        return choice(self.options).perform()  # nosec B311


class _And(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    name: str = ""
    options: tuple[_Action, ...]

    def perform(self) -> list[_AttackResult | _SavingThrowResult]:
        return [option.perform() for option in self.options]
