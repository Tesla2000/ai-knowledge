from __future__ import annotations

from pydantic import BaseModel
from pydantic import Field
from pydantic import NonNegativeInt


class RaceStatistics(BaseModel):
    strength: NonNegativeInt
    dexterity: NonNegativeInt
    constitution: NonNegativeInt
    intelligence: NonNegativeInt
    wisdom: NonNegativeInt
    charisma: NonNegativeInt
    any_of_your_choice: NonNegativeInt = Field(
        description="Typically 'Ability Score Increase: n different ability "
        "scores of your choice increase [...]'"
    )
