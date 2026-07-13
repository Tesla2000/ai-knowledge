from typing import Literal

from dnd.character.blueprint.building_blocks.building_block import BuildingBlock
from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)
from dnd.character.blueprint.states.state import _BPT


class NullBlock(BuildingBlock):
    """A building block that applies no changes to the blueprint.

    Useful as a placeholder or default no-op building block when
    a block is required but no modification is needed.
    """

    type: Literal[BuildingBlockType.NULL_BLOCK] = BuildingBlockType.NULL_BLOCK

    def apply(self, blueprint: _BPT) -> _BPT:
        return blueprint
