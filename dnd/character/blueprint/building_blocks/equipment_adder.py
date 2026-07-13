from typing import Literal

from dnd.character.blueprint.building_blocks.building_block import BuildingBlock
from dnd.character.blueprint.states.state import _BPT
from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)
from pydantic import Field


class EquipmentAdder(BuildingBlock):
    """Adds an item to the character's other equipment list."""

    type: Literal[BuildingBlockType.EQUIPMENT_ADDER] = BuildingBlockType.EQUIPMENT_ADDER

    item: str = Field(description="Equipment item to add to character's inventory")

    def apply(self, blueprint: _BPT) -> _BPT:
        return blueprint.model_copy(
            update={"other_equipment": blueprint.other_equipment + (self.item,)}
        )
