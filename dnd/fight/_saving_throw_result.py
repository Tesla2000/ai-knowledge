from typing import ClassVar

from pydantic import BaseModel, ConfigDict, NonNegativeInt, PositiveInt

from dnd.choices.stats_creation.statistic import Statistic


class _SavingThrowResult(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    dc: PositiveInt
    saving_throw_type: Statistic
    damage_on_fail: NonNegativeInt
    damage_on_success: NonNegativeInt

    def __str__(self) -> str:
        return (
            f"DC {self.dc} {self.saving_throw_type.value} save "
            f"| fail: {self.damage_on_fail} | success: {self.damage_on_success}"
        )
