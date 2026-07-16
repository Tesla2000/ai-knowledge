"""AI-powered stat choice resolver for intelligent ability score increases."""

import json
from dnd.character.blueprint.building_blocks.stat_choice_resolver.base import (
    StatChoiceResolver,
)
from dnd.character.blueprint.building_blocks.building_block import _WideBlueprint
from dnd.choices.stats_creation.statistic import Statistic
from typing import Literal
from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)
from pydantic import BaseModel
from pydantic import Field
from structured_output_creator import OpenAIService, RaisingService


class StatIncreaseSelection(BaseModel):
    """Schema for AI to select stat increases."""

    strength: int = Field(default=0, description="Increase to Strength (0 if none)")
    dexterity: int = Field(default=0, description="Increase to Dexterity (0 if none)")
    constitution: int = Field(
        default=0, description="Increase to Constitution (0 if none)"
    )
    intelligence: int = Field(
        default=0, description="Increase to Intelligence (0 if none)"
    )
    wisdom: int = Field(default=0, description="Increase to Wisdom (0 if none)")
    charisma: int = Field(default=0, description="Increase to Charisma (0 if none)")

    def to_stat_dict(self) -> dict[Statistic, int]:
        return {
            Statistic.STRENGTH: self.strength,
            Statistic.DEXTERITY: self.dexterity,
            Statistic.CONSTITUTION: self.constitution,
            Statistic.INTELLIGENCE: self.intelligence,
            Statistic.WISDOM: self.wisdom,
            Statistic.CHARISMA: self.charisma,
        }


class AIStatChoiceResolver(StatChoiceResolver):
    """AI-powered stat choice resolver that selects stat increases based on character context.

    Uses an LLM to make intelligent decisions about which ability scores to increase
    based on the character's class, current stats, and overall build strategy.

    Example:
        >>> from langchain_openai import ChatOpenAI
        >>> resolver = AIStatChoiceResolver(
        ...     llm=ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
        ... )
    """

    type: Literal[BuildingBlockType.AI_STAT_CHOICE_RESOLVER] = (
        BuildingBlockType.AI_STAT_CHOICE_RESOLVER
    )

    llm: RaisingService[BaseModel] = Field(
        exclude=True,
        default_factory=lambda: RaisingService(service=OpenAIService()),
        description="Language model for making AI-powered decisions",
    )

    def _build_prompt(self, state: _WideBlueprint) -> str:
        n = state.n_stat_choices

        system_prompt = (
            "You are selecting ability score increases for a D&D 5e character.\n"
            f"You have {n} ability score increases to distribute.\n"
            "Choose which ability scores to increase to optimize the character's effectiveness.\n"
        )

        character_description = (
            system_prompt
            + "\n\nCharacter state (JSON):\n"
            + json.dumps(
                {
                    k: v
                    for k, v in state.model_dump(mode="json").items()
                    if v is not None
                },
                indent=2,
            )
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
            "\nReturn the increase amount for each of the six ability scores.",
            "Stats with no increase should be 0.",
        ]

        return character_description + "\n".join(instructions)

    def select_stats_to_increase(self, state: _WideBlueprint) -> dict[Statistic, int]:
        prompt = self._build_prompt(state)

        selection = self.llm.create_structured_output(prompt, StatIncreaseSelection)
        stat_increases = selection.to_stat_dict()

        total_increases = sum(stat_increases.values())
        if total_increases != state.n_stat_choices:
            raise ValueError(
                f"AI distributed {total_increases} increases "
                f"but expected {state.n_stat_choices}"
            )

        for stat, amount in stat_increases.items():
            if amount < 0:
                raise ValueError(
                    f"AI selected negative increase for {stat.value}: {amount}"
                )

        return stat_increases
