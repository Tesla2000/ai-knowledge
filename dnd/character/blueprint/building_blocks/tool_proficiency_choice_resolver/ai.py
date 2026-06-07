"""AI-powered tool proficiency choice resolver."""

from __future__ import annotations

from dnd.character.blueprint.blueprint import Blueprint
from dnd.character.blueprint.blueprint_formatter import (
    BlueprintFormatter,
)
from dnd.character.blueprint.building_blocks.tool_proficiency_choice_resolver.base import (
    ToolProficiencyChoiceResolver,
)
from dnd.other_profficiencies import GamingSet
from dnd.other_profficiencies import MusicalInstrument
from dnd.other_profficiencies import ToolProficiency
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from pydantic import Field


class ToolProficiencySelection(BaseModel):
    """Schema for AI to select tool proficiency replacements."""

    tool_proficiencies: set[
        ToolProficiency | GamingSet | MusicalInstrument
    ] = Field(default_factory=set)


class AIToolProficiencyChoiceResolver(ToolProficiencyChoiceResolver):
    """AI-powered resolver for tool proficiency ANY_OF_YOUR_CHOICE placeholders.

    Uses an LLM to make intelligent tool selections based on
    character context (race, class, background, etc.).

    Example:
        >>> resolver = AIToolProficiencyChoiceResolver(
        ...     llm=ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
        ... )
    """

    llm: ChatOpenAI = Field(
        description="Language model for making AI-powered decisions"
    )

    formatter: BlueprintFormatter = Field(
        default_factory=BlueprintFormatter,
        description="Blueprint formatter for creating AI prompts",
    )

    def _select_tool_proficiency(
        self, available: list[ToolProficiency], _: Blueprint
    ) -> ToolProficiency:
        """Not used in AI implementation - overrides _get_change instead."""
        raise NotImplementedError(
            "AIToolProficiencyChoiceResolver overrides _get_change directly"
        )

    def _select_gaming_set(
        self, available: list[GamingSet], _: Blueprint
    ) -> GamingSet:
        """Not used in AI implementation - overrides _get_change instead."""
        raise NotImplementedError(
            "AIToolProficiencyChoiceResolver overrides _get_change directly"
        )

    def _select_musical_instrument(
        self, available: list[MusicalInstrument], _: Blueprint
    ) -> MusicalInstrument:
        """Not used in AI implementation - overrides _get_change instead."""
        raise NotImplementedError(
            "AIToolProficiencyChoiceResolver overrides _get_change directly"
        )

    def _build_prompt(self, blueprint: Blueprint) -> str:
        """Build a prompt for AI tool proficiency selection.

        Args:
            blueprint: Current character blueprint.

        Returns:
            Formatted prompt string.
        """
        system_prompt = (
            "You are resolving tool proficiency ANY_OF_YOUR_CHOICE "
            "placeholders for a D&D 5e character.\n"
            "Replace each placeholder with the most appropriate tool, "
            "gaming set, or musical instrument based on the character's "
            "race, class, background, and concept.\n"
        )

        character_description = self.formatter.format(
            blueprint, system_prompt=system_prompt
        )

        instructions = ["\n## Placeholders to Resolve\n"]

        # Count tool placeholders
        tool_placeholders = sum(
            1
            for t in blueprint.tool_proficiencies
            if (
                (
                    isinstance(t, ToolProficiency)
                    and t == ToolProficiency.ANY_OF_YOUR_CHOICE
                )
                or (
                    isinstance(t, GamingSet)
                    and t == GamingSet.ANY_OF_YOUR_CHOICE
                )
                or (
                    isinstance(t, MusicalInstrument)
                    and t == MusicalInstrument.ANY_OF_YOUR_CHOICE
                )
            )
        )

        if tool_placeholders == 0:
            return ""  # No placeholders to resolve

        instructions.append(
            f"Tool Proficiencies: {tool_placeholders} ANY_OF_YOUR_CHOICE "
            f"placeholder(s) to replace"
        )
        instructions.append(
            "  Available tool types: ToolProficiency, GamingSet, "
            "MusicalInstrument"
        )

        instructions.append(
            "\n## Selection Instructions\n"
            "Return the complete tool proficiency set with placeholders "
            "replaced by specific choices.\n"
            "Choose tools that best fit the character's class, "
            "background, and concept.\n"
            "Avoid duplicates unless the character already has them."
        )

        return character_description + "\n".join(instructions)

    def get_change(self, blueprint: Blueprint) -> Blueprint:
        """Replace tool proficiency ANY_OF_YOUR_CHOICE placeholders using AI.

        Args:
            blueprint: Current character blueprint.

        Returns:
            Blueprint with tool placeholders replaced by AI selections.
        """
        # Check if there are any placeholders
        has_tool_placeholder = any(
            (
                isinstance(t, ToolProficiency)
                and t == ToolProficiency.ANY_OF_YOUR_CHOICE
            )
            or (isinstance(t, GamingSet) and t == GamingSet.ANY_OF_YOUR_CHOICE)
            or (
                isinstance(t, MusicalInstrument)
                and t == MusicalInstrument.ANY_OF_YOUR_CHOICE
            )
            for t in blueprint.tool_proficiencies
        )

        if not has_tool_placeholder:
            return Blueprint()

        # Build prompt and get AI selection
        prompt = self._build_prompt(blueprint)
        if not prompt:
            return Blueprint()

        structured_llm = self.llm.with_structured_output(
            ToolProficiencySelection
        )
        selection = structured_llm.invoke(prompt)

        # Remove all tool placeholders and add selections
        new_tools = {
            t
            for t in blueprint.tool_proficiencies
            if not (
                (
                    isinstance(t, ToolProficiency)
                    and t == ToolProficiency.ANY_OF_YOUR_CHOICE
                )
                or (
                    isinstance(t, GamingSet)
                    and t == GamingSet.ANY_OF_YOUR_CHOICE
                )
                or (
                    isinstance(t, MusicalInstrument)
                    and t == MusicalInstrument.ANY_OF_YOUR_CHOICE
                )
            )
        }
        new_tools.update(selection.tool_proficiencies)

        return Blueprint(tool_proficiencies=new_tools)
