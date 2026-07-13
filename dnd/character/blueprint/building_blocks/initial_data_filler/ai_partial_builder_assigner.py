from dnd.character.blueprint.building_blocks.building_block import _WideBlueprint
from dnd.character.blueprint.building_blocks.initial_data_filler.ai_builder_base import (
    AIBuilderBase,
)
from dnd.character.blueprint.character_data import CharacterData
from typing import Literal
from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)


class AIPartialBuilderAssigner(AIBuilderBase):
    """Uses AI to fill only unset basic character parameters."""

    type: Literal[BuildingBlockType.AI_PARTIAL_BUILDER_ASSIGNER] = (
        BuildingBlockType.AI_PARTIAL_BUILDER_ASSIGNER
    )

    def compute_character_data(self, blueprint: _WideBlueprint) -> CharacterData:
        prompt = (
            f"Create a D&D 5e character based on this description: {self.description}\n"
            f"The following fields are already set and must be respected: {dict(blueprint)}\n"
            "Only generate values for unset fields."
        )
        result = self._generate_character_template(prompt)
        cd = blueprint.character_data or CharacterData()
        return CharacterData(
            name=cd.name or result.name,
            sex=cd.sex or result.sex,
            age=cd.age or result.age,
            background=cd.background or result.background,
            alignment=cd.alignment or result.alignment,
            backstory=cd.backstory or result.backstory,
            height=cd.height or result.height,
            weight=cd.weight or result.weight,
            eye_color=cd.eye_color or result.eye_color,
            skin_color=cd.skin_color or result.skin_color,
            hairstyle=cd.hairstyle or result.hairstyle,
            appearance=cd.appearance or result.appearance,
            character_traits=cd.character_traits or result.character_traits,
            ideals=cd.ideals or result.ideals,
            bonds=cd.bonds or result.bonds,
            weaknesses=cd.weaknesses or result.weaknesses,
        )
