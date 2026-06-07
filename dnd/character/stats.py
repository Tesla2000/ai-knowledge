from __future__ import annotations

from collections.abc import Mapping
from typing import Self

from dnd.choices.stats_creation.statistic import Statistic
from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import NonNegativeInt


class Stats(BaseModel):
    """D&D character statistics.

    All stats are positive integers representing the character's ability scores.
    Typical range is 1-20 for standard characters, with racial bonuses and
    magical items potentially exceeding this.
    """

    model_config = ConfigDict(frozen=True)

    strength: NonNegativeInt
    dexterity: NonNegativeInt
    constitution: NonNegativeInt
    intelligence: NonNegativeInt
    wisdom: NonNegativeInt
    charisma: NonNegativeInt

    @classmethod
    def from_mapping(cls, mapping: Mapping[Statistic, int]) -> Self:
        return cls(
            strength=mapping[Statistic.STRENGTH],
            dexterity=mapping[Statistic.DEXTERITY],
            constitution=mapping[Statistic.CONSTITUTION],
            intelligence=mapping[Statistic.INTELLIGENCE],
            wisdom=mapping[Statistic.WISDOM],
            charisma=mapping[Statistic.CHARISMA],
        )

    def get_stat(self, stat: Statistic) -> int:
        """Get the value of a specific stat using the Statistic enum."""
        return getattr(self, stat.value.lower())

    def get_modifier(self, stat: Statistic) -> int:
        return getattr(self, stat.value.lower()) // 2 - 5
