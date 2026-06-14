from random import randint
from typing import ClassVar

from pydantic import BaseModel, ConfigDict, NonNegativeInt, PositiveInt

from dnd.fight._attack_result import _AttackResult


class _SpellAttack(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    base_n_dice: PositiveInt
    extra_dice_per_level: NonNegativeInt
    dice_size: PositiveInt
    attack_bonus: int
    damage_bonus: int
    min_level: PositiveInt
    max_level: PositiveInt
    name: str = ""

    def _perform_at_level(self, level: int) -> _AttackResult:
        n_dice = self.base_n_dice + self.extra_dice_per_level * (level - self.min_level)
        roll1 = randint(1, 20)
        roll2 = randint(1, 20)
        return _AttackResult(
            first_roll=roll1 + self.attack_bonus if roll1 != 20 else "critical",
            second_roll=roll2 + self.attack_bonus if roll2 != 20 else "critical",
            damage=sum(randint(1, self.dice_size) for _ in range(n_dice))
            + self.damage_bonus,
            crit_damage=sum(randint(1, self.dice_size) for _ in range(2 * n_dice))
            + self.damage_bonus,
        )

    def perform(self) -> list[_AttackResult]:
        return list(
            map(self._perform_at_level, range(self.min_level, self.max_level + 1))
        )
