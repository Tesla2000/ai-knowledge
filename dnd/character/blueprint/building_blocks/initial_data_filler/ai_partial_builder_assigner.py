from __future__ import annotations

from dnd.character.blueprint.blueprint import Blueprint
from dnd.character.blueprint.building_blocks.initial_data_filler.ai_builder_base import (
    AIBuilderBase,
)


class AIPartialBuilderAssigner(AIBuilderBase):
    """Uses AI to fill only unset basic character parameters.

    This building block leverages LLM structured output to generate values
    only for fields that are currently unset in the blueprint. Already set
    fields are preserved and passed to the AI as context.

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

    def get_change(self, blueprint: Blueprint) -> Blueprint:
        """Generate only unset character parameters using AI.

        Args:
            blueprint: The current blueprint state.

        Yields:
            Blueprint with AI-generated values for unset fields only.
        """
        # Get currently set fields
        set_fields = blueprint.model_dump(exclude_unset=True)

        prompt = (
            f"Create a D&D 5e character based on this description: {self.description}\n"
            f"The following fields are already set and must be respected: {set_fields}\n"
            f"Only generate values for unset fields."
        )
        result = self._generate_character_template(prompt)

        # Only yield fields that aren't already set
        updates = {}
        if "name" not in set_fields:
            updates["name"] = result.name
        if "sex" not in set_fields:
            updates["sex"] = result.sex
        if "age" not in set_fields:
            updates["age"] = result.age
        if "race" not in set_fields:
            updates["race"] = result.race
        if "background" not in set_fields:
            updates["background"] = result.background
        if "alignment" not in set_fields:
            updates["alignment"] = result.alignment
        if "backstory" not in set_fields:
            updates["backstory"] = result.backstory
        if "height" not in set_fields:
            updates["height"] = result.height
        if "weight" not in set_fields:
            updates["weight"] = result.weight
        if "eye_color" not in set_fields:
            updates["eye_color"] = result.eye_color
        if "skin_color" not in set_fields:
            updates["skin_color"] = result.skin_color
        if "hairstyle" not in set_fields:
            updates["hairstyle"] = result.hairstyle
        if "appearance" not in set_fields:
            updates["appearance"] = result.appearance
        if "character_traits" not in set_fields:
            updates["character_traits"] = result.character_traits
        if "ideals" not in set_fields:
            updates["ideals"] = result.ideals
        if "bonds" not in set_fields:
            updates["bonds"] = result.bonds
        if "weaknesses" not in set_fields:
            updates["weaknesses"] = result.weaknesses

        return Blueprint(**updates)
