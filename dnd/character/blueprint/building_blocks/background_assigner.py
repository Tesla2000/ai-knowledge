from __future__ import annotations

from dnd.character.blueprint.blueprint import Blueprint
from dnd.character.blueprint.building_blocks.building_block import (
    BuildingBlock,
)
from dnd.choices.background_creatrion.background import (
    Background,
)
from pydantic import Field


class BackgroundAssigner(BuildingBlock):
    """Assigns a background to the character."""

    background: Background = Field(
        description="Character's background story and origin"
    )

    def get_change(self, blueprint: Blueprint) -> Blueprint:
        """Yield the background difference."""
        return Blueprint(background=self.background)
