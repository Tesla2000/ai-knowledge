"""AI-powered tool proficiency choice resolver."""

from __future__ import annotations

from collections.abc import Generator
from typing import overload

from typing_extensions import deprecated

from dnd.character.blueprint.blueprint_formatter import BlueprintFormatter
from dnd.character.blueprint.state import BlueprintProtocol
from dnd.character.delta.delta import Delta
from dnd.character.blueprint.building_blocks.tool_proficiency_choice_resolver.base import (
    ToolProficiencyChoiceResolver,
    ToolProficienciesDelta,
)
from dnd.character.blueprint.state import HasToolProficiencies
from dnd.other_profficiencies import GamingSet
from dnd.other_profficiencies import MusicalInstrument
from dnd.other_profficiencies import ToolProficiency
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from pydantic import Field
from typing_protocol_intersection import ProtocolIntersection
from typing import Literal
from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)


class ToolProficiencySelection(BaseModel):
    """Schema for AI to select tool proficiency replacements."""

    tool_proficiencies: set[ToolProficiency | GamingSet | MusicalInstrument] = Field(
        default_factory=set
    )


class AIToolProficiencyChoiceResolver(ToolProficiencyChoiceResolver):
    """AI-powered resolver for tool proficiency ANY_OF_YOUR_CHOICE placeholders.

    Uses an LLM to make intelligent tool selections based on
    character context (race, class, background, etc.).

    Example:
        >>> resolver = AIToolProficiencyChoiceResolver(
        ...     llm=ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
        ... )
    """

    type: Literal[BuildingBlockType.AI_TOOL_PROFICIENCY_CHOICE_RESOLVER] = (
        BuildingBlockType.AI_TOOL_PROFICIENCY_CHOICE_RESOLVER
    )

    llm: ChatOpenAI = Field(
        description="Language model for making AI-powered decisions"
    )

    formatter: BlueprintFormatter = Field(
        default_factory=BlueprintFormatter,
        description="Blueprint formatter for creating AI prompts",
    )

    def _select_tool_proficiency(
        self, available: list[ToolProficiency], state: HasToolProficiencies
    ) -> ToolProficiency:
        """Not used — this class overrides get_change directly."""
        raise NotImplementedError(
            "AIToolProficiencyChoiceResolver overrides get_change"
        )

    def _select_gaming_set(
        self, available: list[GamingSet], state: HasToolProficiencies
    ) -> GamingSet:
        """Not used — this class overrides get_change directly."""
        raise NotImplementedError(
            "AIToolProficiencyChoiceResolver overrides get_change"
        )

    def _select_musical_instrument(
        self, available: list[MusicalInstrument], state: HasToolProficiencies
    ) -> MusicalInstrument:
        """Not used — this class overrides get_change directly."""
        raise NotImplementedError(
            "AIToolProficiencyChoiceResolver overrides get_change"
        )

    def _build_prompt(self, state: HasToolProficiencies) -> str:
        system_prompt = (
            "You are resolving tool proficiency ANY_OF_YOUR_CHOICE "
            "placeholders for a D&D 5e character.\n"
            "Replace each placeholder with the most appropriate tool, "
            "gaming set, or musical instrument based on the character's "
            "race, class, background, and concept.\n"
        )

        character_description = self.formatter.format(
            state, system_prompt=system_prompt
        )

        instructions = ["\n## Placeholders to Resolve\n"]

        tool_placeholders = sum(
            1
            for t in state.tool_proficiencies
            if (
                (
                    isinstance(t, ToolProficiency)
                    and t == ToolProficiency.ANY_OF_YOUR_CHOICE
                )
                or (isinstance(t, GamingSet) and t == GamingSet.ANY_OF_YOUR_CHOICE)
                or (
                    isinstance(t, MusicalInstrument)
                    and t == MusicalInstrument.ANY_OF_YOUR_CHOICE
                )
            )
        )

        if tool_placeholders == 0:
            return ""

        instructions.append(
            f"Tool Proficiencies: {tool_placeholders} ANY_OF_YOUR_CHOICE "
            "placeholder(s) to replace"
        )
        instructions.append(
            "  Available tool types: ToolProficiency, GamingSet, MusicalInstrument"
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

    @overload
    def get_change[T: HasToolProficiencies](
        self, state: T
    ) -> Generator[
        ToolProficienciesDelta, None, ProtocolIntersection[T, HasToolProficiencies]
    ]: ...

    @overload
    @deprecated(
        "Pass a state satisfying HasToolProficiencies for precise return typing"
    )
    def get_change[T: BlueprintProtocol](
        self, state: T
    ) -> Generator[Delta, None, BlueprintProtocol]: ...

    def get_change[T: BlueprintProtocol](
        self, state: T
    ) -> Generator[Delta, None, BlueprintProtocol]:
        if not isinstance(state, HasToolProficiencies):
            raise TypeError(
                f"{type(self).__name__} requires HasToolProficiencies, got {type(state).__name__}"
            )
        has_placeholder = any(
            (isinstance(t, ToolProficiency) and t == ToolProficiency.ANY_OF_YOUR_CHOICE)
            or (isinstance(t, GamingSet) and t == GamingSet.ANY_OF_YOUR_CHOICE)
            or (
                isinstance(t, MusicalInstrument)
                and t == MusicalInstrument.ANY_OF_YOUR_CHOICE
            )
            for t in state.tool_proficiencies
        )

        if not has_placeholder:
            delta = ToolProficienciesDelta(
                tool_proficiencies=tuple(state.tool_proficiencies)
            )
            yield delta
            return delta.apply(state)

        prompt = self._build_prompt(state)
        if not prompt:
            delta = ToolProficienciesDelta(
                tool_proficiencies=tuple(state.tool_proficiencies)
            )
            yield delta
            return delta.apply(state)

        structured_llm = self.llm.with_structured_output(ToolProficiencySelection)
        _result = structured_llm.invoke(prompt)
        if not isinstance(_result, ToolProficiencySelection):
            raise TypeError(f"Expected ToolProficiencySelection, got {type(_result)}")
        selection = _result

        new_tools: set[ToolProficiency | GamingSet | MusicalInstrument] = {
            t
            for t in state.tool_proficiencies
            if not (
                (
                    isinstance(t, ToolProficiency)
                    and t == ToolProficiency.ANY_OF_YOUR_CHOICE
                )
                or (isinstance(t, GamingSet) and t == GamingSet.ANY_OF_YOUR_CHOICE)
                or (
                    isinstance(t, MusicalInstrument)
                    and t == MusicalInstrument.ANY_OF_YOUR_CHOICE
                )
            )
        }
        new_tools.update(selection.tool_proficiencies)

        delta = ToolProficienciesDelta(tool_proficiencies=tuple(new_tools))
        yield delta
        return delta.apply(state)
