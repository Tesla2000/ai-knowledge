from typing import Literal

from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)
from dnd.character.blueprint.building_blocks.character_data_field_assigner import (
    CharacterDataFieldAssigner,
)
from dnd.character.blueprint.character_data import CharacterData
from pydantic import Field


class NameAssigner(CharacterDataFieldAssigner):
    """Assigns a name to the character."""

    type: Literal[BuildingBlockType.NAME_ASSIGNER] = BuildingBlockType.NAME_ASSIGNER
    name: str = Field(description="Character's full name")

    def _update(self, character_data: CharacterData) -> CharacterData:
        return character_data.model_copy(update={"name": self.name})
