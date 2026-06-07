from __future__ import annotations

from dnd.character.blueprint.blueprint import Blueprint
from dnd.character.blueprint.building_blocks.building_block import (
    BuildingBlock,
)
from pydantic import Field
from pydantic import PositiveInt


class AgeAssigner(BuildingBlock):
    """Assigns an age to the character."""

    age: PositiveInt = Field(description="Character's age in years")

    def get_change(self, blueprint: Blueprint) -> Blueprint:
        """Yield the age difference."""
        return Blueprint(age=self.age)
