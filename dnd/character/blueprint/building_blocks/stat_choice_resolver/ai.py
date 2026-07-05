"""AI-powered stat choice resolver for intelligent ability score increases."""

from __future__ import annotations

from dnd.character.blueprint.blueprint_formatter import BlueprintFormatter
from dnd.character.blueprint.building_blocks.stat_choice_resolver.base import (
    StatChoiceResolver,
    _StatT,
)
from dnd.choices.stats_creation.statistic import Statistic
from typing import Literal
from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from pydantic import Field


class StatIncreaseSelection(BaseModel):
    """Schema for AI to select stat increases."""

    stat_increases: dict[Statistic, int] = Field(
        description="Dictionary mapping statistics to their increase amounts"
    )


class AIStatChoiceResolver(StatChoiceResolver):
    """AI-powered stat choice resolver that selects stat increases based on character context.

    Uses an LLM to make intelligent decisions about which ability scores to increase
    based on the character's class, current stats, and overall build strategy.

    Example:
        >>> from langchain_openai import ChatOpenAI
        >>> resolver = AIStatChoiceResolver(
        ...     llm=ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
        ... )
        >>> builder = Builder().add(resolver)
    """

    type: Literal[BuildingBlockType.AI_STAT_CHOICE_RESOLVER] = (
        BuildingBlockType.AI_STAT_CHOICE_RESOLVER
    )

    llm: ChatOpenAI = Field(
        description="Language model for making AI-powered decisions"
    )

    formatter: BlueprintFormatter = Field(
        default_factory=BlueprintFormatter,
        description="Blueprint formatter for creating AI prompts",
    )

    def _build_prompt(self, state: _StatT) -> str:
        n = state.n_stat_choices

        system_prompt = (
            "You are selecting ability score increases for a D&D 5e character.\n"
            f"You have {n} ability score increases to distribute.\n"
            "Choose which ability scores to increase to optimize the character's effectiveness.\n"
        )

        character_description = self.formatter.format(
            state, system_prompt=system_prompt
        )

        instructions = [
            "\n## Selection Instructions",
            f"Distribute exactly {n} ability score increases across the six ability scores.",
            "You can apply multiple increases to the same stat (e.g., +2 to one stat).",
            "Consider:",
            "  - Which stats are most important for the character's class",
            "  - Whether to focus on primary stats or shore up weaknesses",
            "  - The character's role in a party (tank, damage dealer, support, etc.)",
            "  - Reaching important stat breakpoints (even numbers for +1 to modifier)",
            "\nReturn a dictionary mapping each stat to its increase amount.",
            "Stats with no increase can be omitted or set to 0.",
        ]

        return character_description + "\n".join(instructions)

    def select_stats_to_increase(self, state: _StatT) -> dict[Statistic, int]:
        prompt = self._build_prompt(state)

        structured_llm = self.llm.with_structured_output(StatIncreaseSelection)
        _result = structured_llm.invoke(prompt)
        if not isinstance(_result, StatIncreaseSelection):
            raise TypeError(f"Expected StatIncreaseSelection, got {type(_result)}")
        selection = _result

        total_increases = sum(selection.stat_increases.values())
        if total_increases != state.n_stat_choices:
            raise ValueError(
                f"AI distributed {total_increases} increases "
                f"but expected {state.n_stat_choices}"
            )

        for stat, amount in selection.stat_increases.items():
            if amount < 0:
                raise ValueError(
                    f"AI selected negative increase for {stat.value}: {amount}"
                )

        return selection.stat_increases
