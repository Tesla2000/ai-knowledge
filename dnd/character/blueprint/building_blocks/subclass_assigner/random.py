"""Random subclass assigner for character creation."""

import random
from typing import Literal
from typing import cast

from dnd.character.blueprint.building_blocks.building_block import BuildingBlock
from dnd.character.blueprint.building_blocks.subclass_assigner.base import (
    _check_can_assign,
)
from dnd.character.blueprint.states.state import _BPT
from dnd.choices.class_creation.character_class import AnySubclass
from dnd.choices.class_creation.character_class import Class
from dnd.choices.class_creation.character_class import SUBCLASSES
from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)
from pydantic import ConfigDict
from pydantic import Field


class RandomSubclassAssigner(BuildingBlock):
    """Randomly selects a subclass from the valid subclasses for the given class."""

    type: Literal[BuildingBlockType.RANDOM_SUBCLASS_ASSIGNER] = (
        BuildingBlockType.RANDOM_SUBCLASS_ASSIGNER
    )

    model_config = ConfigDict(frozen=True)

    class_: Class = Field(
        description="The character class for which to assign a subclass"
    )
    seed: int | None = Field(default=None)

    def apply(self, blueprint: _BPT) -> _BPT:
        _check_can_assign(self.class_, blueprint.classes)
        subclass_enum = SUBCLASSES[self.class_]
        for existing in blueprint.subclasses:
            if isinstance(existing, subclass_enum):
                return blueprint
        random.seed(self.seed)
        selected = cast(AnySubclass, random.choice(tuple(subclass_enum)))
        return blueprint.model_copy(
            update={"subclasses": blueprint.subclasses + (selected,)}
        )
