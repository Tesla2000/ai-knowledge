from __future__ import annotations

from dnd.character.blueprint.blueprint import Blueprint
from dnd.character.blueprint.building_blocks.building_block import (
    BuildingBlock,
)
from pydantic import Field


class LevelAssigner(BuildingBlock):
    """Assigns a level to the character."""

    level: int = Field(ge=1, le=20, description="Character's level (1-20)")

    def get_change(self, blueprint: Blueprint) -> Blueprint:
        """Yield the level difference."""
        return Blueprint(level=self.level)
