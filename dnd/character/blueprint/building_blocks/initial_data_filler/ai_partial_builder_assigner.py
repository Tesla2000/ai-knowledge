from __future__ import annotations

from collections.abc import Generator

from dnd.character.blueprint.building_blocks.initial_data_filler.ai_builder_base import (
    AIBuilderBase,
)
from dnd.character.blueprint.state import BlueprintProtocol
from dnd.character.blueprint.state import HasAge
from dnd.character.blueprint.state import HasAlignment
from dnd.character.blueprint.state import HasAppearance
from dnd.character.blueprint.state import HasBackground
from dnd.character.blueprint.state import HasBackstory
from dnd.character.blueprint.state import HasBonds
from dnd.character.blueprint.state import HasCharacterTraits
from dnd.character.blueprint.state import HasEyeColor
from dnd.character.blueprint.state import HasHairstyle
from dnd.character.blueprint.state import HasHeight
from dnd.character.blueprint.state import HasIdeals
from dnd.character.blueprint.state import HasInitialData
from dnd.character.blueprint.state import HasName
from dnd.character.blueprint.state import HasSex
from dnd.character.blueprint.state import HasSkinColor
from dnd.character.blueprint.state import HasWeaknesses
from dnd.character.blueprint.state import HasWeight
from dnd.character.delta.initial_data_delta import InitialDataDelta


class AIPartialBuilderAssigner(AIBuilderBase):
    """Uses AI to fill only unset basic character parameters.

    Leverages LLM structured output to generate values only for fields that are
    currently unset in the blueprint. Already set fields are preserved and
    passed to the AI as context.

    Example:
        >>> from langchain_openai import ChatOpenAI
        >>> builder = Builder([
        ...     RaceAssigner(race=Race.ELF),  # Set race first
        ...     AIPartialBuilderAssigner(
        ...         description="A wise wizard",
        ...         llm=ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
        ...     ),  # AI fills other fields, respects race=ELF
        ... ])
        >>> character = builder.build()
    """

    def get_change(
        self, state: BlueprintProtocol
    ) -> Generator[InitialDataDelta, None, HasInitialData]:
        prompt = (
            f"Create a D&D 5e character based on this description: {self.description}\n"
            f"The following fields are already set and must be respected: {dict(state)}\n"
            "Only generate values for unset fields."
        )
        result = self._generate_character_template(prompt)

        delta = InitialDataDelta(
            name=state.name if isinstance(state, HasName) else result.name,
            sex=state.sex if isinstance(state, HasSex) else result.sex,
            age=state.age if isinstance(state, HasAge) else result.age,
            background=state.background
            if isinstance(state, HasBackground)
            else result.background,
            alignment=state.alignment
            if isinstance(state, HasAlignment)
            else result.alignment,
            backstory=state.backstory
            if isinstance(state, HasBackstory)
            else result.backstory,
            height=state.height if isinstance(state, HasHeight) else result.height,
            weight=state.weight if isinstance(state, HasWeight) else result.weight,
            eye_color=state.eye_color
            if isinstance(state, HasEyeColor)
            else result.eye_color,
            skin_color=state.skin_color
            if isinstance(state, HasSkinColor)
            else result.skin_color,
            hairstyle=state.hairstyle
            if isinstance(state, HasHairstyle)
            else result.hairstyle,
            appearance=state.appearance
            if isinstance(state, HasAppearance)
            else result.appearance,
            character_traits=state.character_traits
            if isinstance(state, HasCharacterTraits)
            else result.character_traits,
            ideals=state.ideals if isinstance(state, HasIdeals) else result.ideals,
            bonds=state.bonds if isinstance(state, HasBonds) else result.bonds,
            weaknesses=state.weaknesses
            if isinstance(state, HasWeaknesses)
            else result.weaknesses,
        )
        yield delta
        return delta.apply(state)
