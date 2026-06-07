from dnd.character.blueprint.blueprint import Blueprint
from dnd.character.blueprint.building_blocks.building_block import (
    BuildingBlock,
)


class NullBlock(BuildingBlock):
    """A building block that applies no changes to the blueprint.

    Useful as a placeholder or default no-op building block when
    a block is required but no modification is needed.
    """

    def get_change(self, blueprint: Blueprint) -> Blueprint:
        """Return an empty Blueprint (no changes)."""
        return Blueprint()
