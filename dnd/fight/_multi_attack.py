from typing import ClassVar

from pydantic import BaseModel, ConfigDict

from dnd.fight._attack import _Attack
from dnd.fight._attack_result import _AttackResult


class _MultiAttack(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    attacks: tuple[_Attack, ...]
    name: str = ""

    def perform(self) -> list[_AttackResult]:
        return [attack.perform() for attack in self.attacks]
