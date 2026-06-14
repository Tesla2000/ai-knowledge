from random import randint
from typing import ClassVar

from pydantic import BaseModel, ConfigDict, PositiveInt

from dnd.choices.stats_creation.statistic import Statistic
from dnd.fight._saving_throw_result import _SavingThrowResult


class _SavingThrow(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    n_dice: PositiveInt
    dice_size: PositiveInt
    damage_bonus: int
    dc: PositiveInt
    name: str
    saving_throw_type: Statistic
    half_on_success: bool = True

    def perform(self) -> _SavingThrowResult:
        total = (
            sum(randint(1, self.dice_size) for _ in range(self.n_dice))
            + self.damage_bonus
        )
        return _SavingThrowResult(
            dc=self.dc,
            saving_throw_type=self.saving_throw_type,
            damage_on_fail=total,
            damage_on_success=total // 2 if self.half_on_success else 0,
        )
