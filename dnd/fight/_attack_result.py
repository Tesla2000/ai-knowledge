from typing import ClassVar

from pydantic import BaseModel, ConfigDict, NonNegativeInt


class _AttackResult(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    first_roll: int | str
    second_roll: int | str
    damage: NonNegativeInt
    crit_damage: NonNegativeInt
