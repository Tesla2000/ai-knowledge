from __future__ import annotations

from dnd.character.blueprint.blueprint import Blueprint
from dnd.character.blueprint.building_blocks.building_block import (
    BuildingBlock,
)
from pydantic import Field


class NameAssigner(BuildingBlock):
    """Assigns a name to the character."""

    name: str = Field(description="Character's full name")

    def get_change(self, blueprint: Blueprint) -> Blueprint:
        """Yield the name difference."""
        return Blueprint(name=self.name)
