"""AI-powered subclass assigner for intelligent subclass selection."""

from __future__ import annotations

from dnd.character.blueprint.blueprint import Blueprint
from dnd.character.blueprint.blueprint_formatter import (
    BlueprintFormatter,
)
from dnd.character.blueprint.building_blocks.subclass_assigner.base import (
    SubclassAssigner,
)
from dnd.choices.class_creation.character_class import (
    AnySubclass,
)
from dnd.choices.class_creation.character_class import (
    SUBCLASSES,
)
from langchain_openai import ChatOpenAI  # type: ignore[import-not-found]
from pydantic import create_model
from pydantic import Field


class AISubclassAssigner(SubclassAssigner):
    """AI-powered subclass assigner that selects subclasses based on character context.

    Uses an LLM to make intelligent subclass selections based on the character's
    background, stats, personality, and overall concept. The AI considers which
    subclass best fits the character's thematic and mechanical direction.

    Example:
        >>> from dnd.choices.class_creation.character_class import Class
        >>> from langchain_openai import ChatOpenAI
        >>> assigner = AISubclassAssigner(
        ...     class_=Class.WIZARD,
        ...     llm=ChatOpenAI(model="gpt-4o-mini", temperature=0.4)
        ... )
        >>> builder = Builder().add(assigner)
    """

    llm: ChatOpenAI = Field(
        description="Language model for making AI-powered decisions"
    )

    formatter: BlueprintFormatter = Field(
        default_factory=BlueprintFormatter,
        description="Blueprint formatter for creating AI prompts",
    )

    def _build_prompt(self, blueprint: Blueprint) -> str:
        """Build a prompt for AI subclass selection.

        Args:
            blueprint: Current character blueprint.

        Returns:
            Formatted prompt string.
        """
        system_prompt = (
            f"You are selecting a subclass for a D&D 5e {self.class_.value}.\n"
            "Choose the subclass that best fits the character's:\n"
            "  - Background and backstory\n"
            "  - Personality and ideals\n"
            "  - Ability score distribution\n"
            "  - Overall character concept and theme\n"
            "\nThe subclass should feel like a natural extension of who this character is.\n"
        )

        # Use formatter with custom system prompt
        character_description = self.formatter.format(
            blueprint, system_prompt=system_prompt
        )

        # Add subclass options section
        subclass_instructions = [
            f"\n## Available {self.class_.value} Subclasses",
            "Select ONE subclass from the following options:\n",
        ]

        for subclass_option in self.available_subclasses:
            subclass_instructions.append(f"  - {subclass_option.value}")

        subclass_instructions.append(
            "\n## Selection Instructions\n"
            "Return exactly one subclass from the list above.\n"
            "Consider which subclass:\n"
            "  - Aligns with the character's backstory and motivations\n"
            "  - Complements their ability scores and playstyle\n"
            "  - Fits their personality and moral alignment\n"
            "  - Makes thematic sense for their background"
        )

        return character_description + "\n".join(subclass_instructions)

    def _select_subclass(self, blueprint: Blueprint) -> AnySubclass:
        """Use AI to select a subclass for the character.

        Args:
            blueprint: Current character blueprint.

        Returns:
            AI-selected subclass.
        """
        # Build prompt and get AI selection
        prompt = self._build_prompt(blueprint)

        # Create dynamic response model for this class's subclasses
        subclass_enum = SUBCLASSES[self.class_]
        SubclassSelection = create_model(
            f"{self.class_.value}SubclassSelection",
            subclass=(subclass_enum, ...),
        )

        structured_llm = self.llm.with_structured_output(SubclassSelection)

        try:
            result = structured_llm.invoke(prompt)
        except Exception as e:
            raise ValueError(
                f"AI failed to select subclass for {self.class_.value}: {e}"
            ) from e

        return result.subclass  # type: ignore[no-any-return]
