"""AI-powered tool proficiency choice resolver."""

from dnd.character.blueprint.formatter import BlueprintFormatter
from dnd.character.blueprint.building_blocks.tool_proficiency_choice_resolver.base import (
    ToolProficiencyChoiceResolver,
)
from dnd.character.blueprint.building_blocks.building_block import _WideBlueprint
from dnd.character.blueprint.states.state import _BPT
from dnd.other_profficiencies import GamingSet
from dnd.other_profficiencies import MusicalInstrument
from dnd.other_profficiencies import ToolProficiency
from pydantic import BaseModel
from pydantic import Field
from structured_output_creator import OpenAIService, RaisingService
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
    """AI-powered resolver for tool proficiency ANY_OF_YOUR_CHOICE placeholders."""

    type: Literal[BuildingBlockType.AI_TOOL_PROFICIENCY_CHOICE_RESOLVER] = (
        BuildingBlockType.AI_TOOL_PROFICIENCY_CHOICE_RESOLVER
    )

    llm: RaisingService = Field(
        default_factory=lambda: RaisingService(service=OpenAIService())
    )
    formatter: BlueprintFormatter = Field(default_factory=BlueprintFormatter)

    def select_tool_proficiency(
        self,
        available: list[ToolProficiency],
        tool_proficiencies: tuple[ToolProficiency | GamingSet | MusicalInstrument, ...],
    ) -> ToolProficiency:
        raise NotImplementedError("AIToolProficiencyChoiceResolver overrides apply")

    def select_gaming_set(
        self,
        available: list[GamingSet],
        tool_proficiencies: tuple[ToolProficiency | GamingSet | MusicalInstrument, ...],
    ) -> GamingSet:
        raise NotImplementedError("AIToolProficiencyChoiceResolver overrides apply")

    def select_musical_instrument(
        self,
        available: list[MusicalInstrument],
        tool_proficiencies: tuple[ToolProficiency | GamingSet | MusicalInstrument, ...],
    ) -> MusicalInstrument:
        raise NotImplementedError("AIToolProficiencyChoiceResolver overrides apply")

    def _build_prompt(self, blueprint: _WideBlueprint) -> str:
        system_prompt = "You are resolving tool proficiency ANY_OF_YOUR_CHOICE placeholders for a D&D 5e character.\n"
        character_description = self.formatter.format(
            blueprint, system_prompt=system_prompt
        )
        not_choice = {
            ToolProficiency.ANY_OF_YOUR_CHOICE,
            GamingSet.ANY_OF_YOUR_CHOICE,
            MusicalInstrument.ANY_OF_YOUR_CHOICE,
        }
        tool_placeholders = sum(
            1 for t in blueprint.tool_proficiencies if t in not_choice
        )
        if tool_placeholders == 0:
            return ""
        return (
            character_description
            + f"\n## Tool Proficiencies to Choose ({tool_placeholders})"
        )

    def apply(self, blueprint: _BPT) -> _BPT:
        not_choice = {
            ToolProficiency.ANY_OF_YOUR_CHOICE,
            GamingSet.ANY_OF_YOUR_CHOICE,
            MusicalInstrument.ANY_OF_YOUR_CHOICE,
        }
        has_placeholder = any(t in not_choice for t in blueprint.tool_proficiencies)

        if not has_placeholder:
            return blueprint

        prompt = self._build_prompt(blueprint)
        if not prompt:
            return blueprint

        selection = self.llm.create_structured_output(prompt, ToolProficiencySelection)
        new_tools: set[ToolProficiency | GamingSet | MusicalInstrument] = {
            t for t in blueprint.tool_proficiencies if t not in not_choice
        }
        new_tools.update(selection.tool_proficiencies)
        return blueprint.model_copy(update={"tool_proficiencies": tuple(new_tools)})
