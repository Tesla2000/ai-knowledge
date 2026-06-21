from __future__ import annotations

from abc import ABC

from dnd.character.blueprint.building_blocks.character_base_template import (
    CharacterBaseTemplate,
)
from dnd.character.blueprint.building_blocks.initial_data_filler.base_filler import (
    InitialDataFiller,
)
from langchain_openai import ChatOpenAI
from pydantic import Field


class AIBuilderBase(InitialDataFiller, ABC):
    """Base class for AI-powered character builders.

    Provides common functionality for AI building blocks that use LLM
    structured output to generate character parameters from descriptions.
    """

    description: str = Field(
        description="Natural language description of the character to generate"
    )

    llm: ChatOpenAI = Field(
        description="Language model for making AI-powered decisions"
    )

    def _generate_character_template(self, prompt: str) -> CharacterBaseTemplate:
        """Generate character parameters using AI.

        Args:
            prompt: The prompt to send to the AI.

        Returns:
            CharacterBaseTemplate with AI-generated values.
        """
        template = self.llm.with_structured_output(CharacterBaseTemplate)
        result = template.invoke(prompt)
        if not isinstance(result, CharacterBaseTemplate):
            raise TypeError(f"Expected CharacterBaseTemplate, got {type(result)}")
        return result
