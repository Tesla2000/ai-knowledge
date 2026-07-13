from typing import Literal

from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)
from dnd.character.blueprint.building_blocks.character_data_field_assigner import (
    CharacterDataFieldAssigner,
)
from dnd.character.blueprint.character_data import CharacterData
from dnd.choices.background_creatrion.background import Background
from pydantic import Field


class BackgroundAssigner(CharacterDataFieldAssigner):
    """Assigns a background to the character."""

    type: Literal[BuildingBlockType.BACKGROUND_ASSIGNER] = (
        BuildingBlockType.BACKGROUND_ASSIGNER
    )
    background: Background = Field(description="Character's background")

    def _update(self, character_data: CharacterData) -> CharacterData:
        return character_data.model_copy(update={"background": self.background})
