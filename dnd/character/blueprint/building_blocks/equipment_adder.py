from __future__ import annotations

from dnd.character.blueprint.blueprint import Blueprint
from dnd.character.blueprint.building_blocks.building_block import (
    BuildingBlock,
)
from pydantic import Field


class EquipmentAdder(BuildingBlock):
    """Adds an item to the character's other equipment list.

    Appends to existing equipment. Allows duplicates.

    Example:
        >>> builder = Builder([
        ...     EquipmentAdder(item="Rope, hempen (50 feet)"),
        ...     EquipmentAdder(item="Torch"),
        ...     EquipmentAdder(item="Torch"),  # Second torch
        ...     EquipmentAdder(item="Healing potion"),
        ... ])
    """

    item: str = Field(description="Equipment item to add to character's inventory")

    def get_change(self, blueprint: Blueprint) -> Blueprint:
        """Add the item to the existing equipment tuple.

        Args:
            blueprint: The current blueprint state.

        Yields:
            Blueprint with the item added.
        """
        existing_equipment = blueprint.other_equipment
        new_equipment = existing_equipment + (self.item,)
        return Blueprint(other_equipment=new_equipment)
