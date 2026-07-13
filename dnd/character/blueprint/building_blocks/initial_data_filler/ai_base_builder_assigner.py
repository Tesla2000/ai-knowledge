from dnd.character.blueprint.building_blocks.building_block import _WideBlueprint
from dnd.character.blueprint.building_blocks.initial_data_filler.ai_builder_base import (
    AIBuilderBase,
)
from dnd.character.blueprint.character_data import CharacterData
from typing import Literal
from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)


class AIBaseBuilderAssigner(AIBuilderBase):
    """Uses AI to assign all basic character parameters based on a description."""

    type: Literal[BuildingBlockType.AI_BASE_BUILDER_ASSIGNER] = (
        BuildingBlockType.AI_BASE_BUILDER_ASSIGNER
    )

    def compute_character_data(self, blueprint: _WideBlueprint) -> CharacterData:
        prompt = (
            f"Create a D&D 5e character based on this description: {self.description}\n"
            f"Here are current values: {dict(blueprint)}"
        )
        result = self._generate_character_template(prompt)
        return CharacterData(
            name=result.name,
            sex=result.sex,
            age=result.age,
            background=result.background,
            alignment=result.alignment,
            backstory=result.backstory,
            height=result.height,
            weight=result.weight,
            eye_color=result.eye_color,
            skin_color=result.skin_color,
            hairstyle=result.hairstyle,
            appearance=result.appearance,
            character_traits=result.character_traits,
            ideals=result.ideals,
            bonds=result.bonds,
            weaknesses=result.weaknesses,
        )
