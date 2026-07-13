from typing import Literal

from dnd.character.blueprint.building_blocks.building_block import BuildingBlock
from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)
from dnd.character.blueprint.building_blocks.subclass_assigner.ai import (
    AISubclassAssigner,
)
from dnd.character.blueprint.building_blocks.subclass_assigner.base import CanNotAssign
from dnd.character.blueprint.building_blocks.subclass_assigner.random import (
    RandomSubclassAssigner,
)
from dnd.character.blueprint.states.state import _BPT
from pydantic import Field


class OptionalSubclassAssigner(BuildingBlock):
    """Optionally assigns a subclass, silently skipping if assignment is not possible."""

    type: Literal[BuildingBlockType.OPTIONAL_SUBCLASS_ASSIGNER] = (
        BuildingBlockType.OPTIONAL_SUBCLASS_ASSIGNER
    )

    assigner: RandomSubclassAssigner | AISubclassAssigner = Field(
        description="The subclass assigner strategy to use"
    )

    def apply(self, blueprint: _BPT) -> _BPT:
        try:
            return self.assigner.apply(blueprint)
        except CanNotAssign:
            return blueprint
