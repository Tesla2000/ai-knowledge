from typing import Literal

from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)
from dnd.character.blueprint.building_blocks.character_data_field_assigner import (
    CharacterDataFieldAssigner,
)
from dnd.character.blueprint.character_data import CharacterData
from dnd.choices.alignment import Alignment
from pydantic import Field


class AlignmentAssigner(CharacterDataFieldAssigner):
    """Assigns an alignment to the character."""

    type: Literal[BuildingBlockType.ALIGNMENT_ASSIGNER] = (
        BuildingBlockType.ALIGNMENT_ASSIGNER
    )
    alignment: Alignment = Field(description="Character's moral alignment")

    def _update(self, character_data: CharacterData) -> CharacterData:
        return character_data.model_copy(update={"alignment": self.alignment})
