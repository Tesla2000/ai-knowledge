from typing import ClassVar

from pydantic import BaseModel, ConfigDict, NonNegativeInt


class _AttackResult(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    first_roll: int | str
    second_roll: int | str
    damage: NonNegativeInt
    crit_damage: NonNegativeInt

    def __str__(self) -> str:
        first_crit = self.first_roll == "critical"
        second_crit = self.second_roll == "critical"
        base = (
            f"first_roll={self.first_roll!r} second_roll={self.second_roll!r}"
            f" damage={self.damage}"
        )
        if first_crit and second_crit:
            return f"{base} | crit with disadvantage: {self.crit_damage}"
        if first_crit:
            return f"{base} | crit: {self.crit_damage}"
        if second_crit:
            return f"{base} | crit with adv: {self.crit_damage}"
        return base
