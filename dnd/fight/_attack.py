from random import randint
from typing import ClassVar

from pydantic import BaseModel, ConfigDict, PositiveInt

from dnd.fight._attack_result import _AttackResult


class _Attack(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    n_dice: PositiveInt
    dice_size: PositiveInt
    attack_bonus: int
    damage_bonus: int
    name: str = ""

    def perform(self) -> _AttackResult:
        roll1 = randint(1, 20)
        roll2 = randint(1, 20)
        return _AttackResult(
            first_roll=roll1 + self.attack_bonus if roll1 != 20 else "critical",
            second_roll=roll2 + self.attack_bonus if roll2 != 20 else "critical",
            damage=sum(randint(1, self.dice_size) for _ in range(self.n_dice))
            + self.damage_bonus,
            crit_damage=sum(randint(1, self.dice_size) for _ in range(2 * self.n_dice))
            + self.damage_bonus,
        )
