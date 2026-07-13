from typing import Literal

from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)
from dnd.character.blueprint.building_blocks.character_data_field_assigner import (
    CharacterDataFieldAssigner,
)
from dnd.character.blueprint.character_data import CharacterData
from dnd.choices.sex import Sex
from pydantic import Field


class SexAssigner(CharacterDataFieldAssigner):
    """Assigns a sex to the character."""

    type: Literal[BuildingBlockType.SEX_ASSIGNER] = BuildingBlockType.SEX_ASSIGNER
    sex: Sex = Field(description="Character's biological sex")

    def _update(self, character_data: CharacterData) -> CharacterData:
        return character_data.model_copy(update={"sex": self.sex})
