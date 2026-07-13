from typing import Literal

from dnd.character.blueprint.building_blocks.building_block import BuildingBlock
from dnd.character.blueprint.states.state import _BPT
from dnd.choices.equipment_creation.weapons import WeaponName
from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)
from pydantic import Field


class WeaponAdder(BuildingBlock):
    """Adds a weapon to the character's weapons list."""

    type: Literal[BuildingBlockType.WEAPON_ADDER] = BuildingBlockType.WEAPON_ADDER

    weapon: WeaponName = Field(description="Weapon to add to character's inventory")

    def apply(self, blueprint: _BPT) -> _BPT:
        return blueprint.model_copy(
            update={"weapons": blueprint.weapons + (self.weapon,)}
        )
