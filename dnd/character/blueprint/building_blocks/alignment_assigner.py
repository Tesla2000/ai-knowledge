from __future__ import annotations

from dnd.character.blueprint.blueprint import Blueprint
from dnd.character.blueprint.building_blocks.building_block import (
    BuildingBlock,
)
from dnd.choices.alignment import Alignment
from pydantic import Field


class AlignmentAssigner(BuildingBlock):
    """Assigns an alignment to the character."""

    alignment: Alignment = Field(description="Character's moral and ethical alignment")

    def get_change(self, blueprint: Blueprint) -> Blueprint:
        """Yield the alignment difference."""
        return Blueprint(alignment=self.alignment)
