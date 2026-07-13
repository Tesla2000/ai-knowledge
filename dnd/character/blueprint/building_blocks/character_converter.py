from typing import Literal

from dnd.character.blueprint.building_blocks.building_block import BuildingBlock
from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)
from dnd.character.blueprint.states.convertible_blueprint import ConvertibleBlueprint
from dnd.character.presentable_character import PresentableCharacter
from pydantic import ConfigDict


class CharacterConverter(BuildingBlock):
    """Seals a fully resolved ConvertibleBlueprint into a PresentableCharacter."""

    model_config = ConfigDict(frozen=True)

    type: Literal[BuildingBlockType.CHARACTER_CONVERTER] = (
        BuildingBlockType.CHARACTER_CONVERTER
    )

    def apply(self, blueprint: ConvertibleBlueprint) -> PresentableCharacter:
        return blueprint.to_presentable_character()
