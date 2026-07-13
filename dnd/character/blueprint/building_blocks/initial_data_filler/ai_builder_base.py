from abc import ABC

from dnd.character.blueprint.building_blocks.character_base_template import (
    CharacterBaseTemplate,
)
from dnd.character.blueprint.building_blocks.initial_data_filler.base_filler import (
    InitialDataFiller,
)
from pydantic import Field
from structured_output_creator import OpenAIService, RaisingService


class AIBuilderBase(InitialDataFiller, ABC):
    """Base class for AI-powered character builders.

    Provides common functionality for AI building blocks that use LLM
    structured output to generate character parameters from descriptions.
    """

    description: str = Field(
        description="Natural language description of the character to generate"
    )

    llm: RaisingService = Field(
        default_factory=lambda: RaisingService(service=OpenAIService()),
        description="Language model for making AI-powered decisions",
    )

    def _generate_character_template(self, prompt: str) -> CharacterBaseTemplate:
        return self.llm.create_structured_output(prompt, CharacterBaseTemplate)
