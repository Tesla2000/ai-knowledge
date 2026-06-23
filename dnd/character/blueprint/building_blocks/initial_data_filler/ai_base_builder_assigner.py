from __future__ import annotations

from collections.abc import Generator

from dnd.character.blueprint.building_blocks.initial_data_filler.ai_builder_base import (
    AIBuilderBase,
)
from dnd.character.blueprint.state import BlueprintProtocol
from dnd.character.blueprint.state import HasInitialData
from dnd.character.delta.initial_data_delta import InitialDataDelta


class AIBaseBuilderAssigner(AIBuilderBase):
    """Uses AI to assign all basic character parameters based on a description.

    Leverages LLM structured output to generate coherent character parameters
    (name, sex, age, background, alignment, backstory, physical attributes, and
    personality traits) from a natural language description. Always generates all
    fields regardless of what's already set.

    Example:
        >>> from langchain_openai import ChatOpenAI
        >>> assigner = AIBaseBuilderAssigner(
        ...     description="A wise elderly elven wizard who studies ancient magic",
        ...     llm=ChatOpenAI(model="gpt-4o", temperature=0.7)
        ... )
        >>> builder = Builder([assigner])
        >>> character = builder.build()
    """

    def get_change(
        self, state: BlueprintProtocol
    ) -> Generator[InitialDataDelta, None, HasInitialData]:
        prompt = (
            f"Create a D&D 5e character based on this description: {self.description}\n"
            f"Here are current values: {dict(state)}"
        )
        result = self._generate_character_template(prompt)

        delta = InitialDataDelta(
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
        yield delta
        return delta.apply(state)
