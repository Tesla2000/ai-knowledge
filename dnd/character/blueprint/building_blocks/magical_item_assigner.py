from __future__ import annotations

from dnd.character.blueprint.blueprint import Blueprint
from dnd.character.blueprint.building_blocks.building_block import (
    BuildingBlock,
)
from dnd.character.magical_item.item import MagicalItem
from pydantic import Field


class MagicalItemAssigner(BuildingBlock):
    """Building block that assigns a magical item to a character blueprint.

    Wraps a MagicalItem object and applies it to the blueprint using the
    item's assign_to method, which determines what changes are made.
    """

    magical_item: MagicalItem = Field(
        description="Magical item to assign to the character"
    )

    def get_change(self, blueprint: Blueprint) -> Blueprint:
        return self.magical_item.assign_to(blueprint)
