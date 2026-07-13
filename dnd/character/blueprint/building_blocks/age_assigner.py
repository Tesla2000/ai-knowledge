from typing import Literal

from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)
from dnd.character.blueprint.building_blocks.character_data_field_assigner import (
    CharacterDataFieldAssigner,
)
from dnd.character.blueprint.character_data import CharacterData
from pydantic import Field
from pydantic import PositiveInt


class AgeAssigner(CharacterDataFieldAssigner):
    """Assigns an age to the character."""

    type: Literal[BuildingBlockType.AGE_ASSIGNER] = BuildingBlockType.AGE_ASSIGNER
    age: PositiveInt = Field(description="Character's age in years")

    def _update(self, character_data: CharacterData) -> CharacterData:
        return character_data.model_copy(update={"age": self.age})
