from typing import Literal

from dnd.character.blueprint.building_blocks.building_block import BuildingBlock
from dnd.character.blueprint.states.state import _BPT
from dnd.character.feature.feature import Feature
from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)
from pydantic import Field


class FeatureAssigner(BuildingBlock):
    """Building block that assigns a feature to a character blueprint.

    Example:
        >>> trance = Feature(...)
        >>> trance_assigner = FeatureAssigner(feature=trance)
    """

    type: Literal[BuildingBlockType.FEATURE_ASSIGNER] = (
        BuildingBlockType.FEATURE_ASSIGNER
    )

    feature: Feature = Field(
        description="Character feature to assign (ability, trait, or stat boost)"
    )

    def apply(self, blueprint: _BPT) -> _BPT:
        return blueprint
