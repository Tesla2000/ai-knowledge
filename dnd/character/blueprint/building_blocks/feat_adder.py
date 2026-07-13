from typing import Literal

from dnd.character.blueprint.building_blocks.building_block import BuildingBlock
from dnd.character.blueprint.building_blocks.building_block import _WideBlueprint
from dnd.character.feature.feats import FeatName
from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)
from pydantic import Field


class FeatAdder(BuildingBlock):
    """Adds a feat to the character's feat list."""

    type: Literal[BuildingBlockType.FEAT_ADDER] = BuildingBlockType.FEAT_ADDER

    feat: FeatName = Field(description="Feat to add to character's feat list")

    def apply(self, blueprint: _WideBlueprint) -> _WideBlueprint:
        if self.feat in blueprint.feats:
            raise ValueError(f"Feat {self.feat} already exists in character feats")
        return blueprint.model_copy(update={"feats": blueprint.feats + (self.feat,)})
