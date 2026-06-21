"""AI-powered feat choice resolver."""

from __future__ import annotations

from dnd.character.blueprint.blueprint import Blueprint
from dnd.character.blueprint.blueprint_formatter import (
    BlueprintFormatter,
)
from dnd.character.blueprint.building_blocks.feat_choice_resolver.base import (
    FeatChoiceResolver,
)
from dnd.character.feature.feats import FeatName
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from pydantic import Field


class FeatSelection(BaseModel):
    """Schema for AI to select feat replacements."""

    feats: set[FeatName] = Field(default_factory=set)


class AIFeatChoiceResolver(FeatChoiceResolver):
    """AI-powered resolver for FeatName.ANY_OF_YOUR_CHOICE placeholders.

    Uses an LLM to make intelligent feat selections based on
    character context (race, class, stats, etc.).

    Example:
        >>> resolver = AIFeatChoiceResolver(
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

    def select_from_available(
        self, available: list[FeatName], _: Blueprint
    ) -> FeatName:
        """Not used in AI implementation - overrides _get_change instead."""
        raise NotImplementedError("AIFeatChoiceResolver overrides _get_change directly")

    def _build_prompt(self, blueprint: Blueprint) -> str:
        """Build a prompt for AI feat selection.

        Args:
            blueprint: Current character blueprint.

        Returns:
            Formatted prompt string.
        """
        system_prompt = (
            "You are resolving FeatName.ANY_OF_YOUR_CHOICE placeholders "
            "for a D&D 5e character.\n"
            "Replace each placeholder with the most appropriate feat "
            "based on the character's race, class, stats, and concept.\n"
        )

        character_description = self.formatter.format(
            blueprint, system_prompt=system_prompt
        )

        instructions = ["\n## Placeholders to Resolve\n"]

        # Count feat placeholders
        count = sum(map(list(blueprint.feats).count, FeatName.not_choosables()))
        if count == 0:
            return ""  # No placeholders to resolve

        instructions.append(
            f"Feats: {count} ANY_OF_YOUR_CHOICE placeholder(s) to replace"
        )

        # Check if ASI is allowed (level 2+)
        ability_score_improvement_allowed = sum(blueprint.classes.values()) != 1

        # Build available feats list
        available_feats = [
            f.value
            for f in FeatName
            if f not in FeatName.not_choosables()
            and (
                ability_score_improvement_allowed or f not in FeatName.not_choosables()
            )
        ]
        instructions.append(f"  Available: {', '.join(available_feats)}")

        if not ability_score_improvement_allowed:
            instructions.append(
                "  Note: ABILITY_SCORE_IMPROVEMENT is not available at level 1"
            )

        instructions.append(
            "\n## Selection Instructions\n"
            "Return the complete feat set with placeholders replaced "
            "by specific choices.\n"
            "Choose feats that best fit the character's class, "
            "stats, and combat style.\n"
            "Avoid duplicates unless the character already has them."
        )

        return character_description + "\n".join(instructions)

    def get_change(self, blueprint: Blueprint) -> Blueprint:
        """Replace FeatName.ANY_OF_YOUR_CHOICE placeholders using AI.

        Args:
            blueprint: Current character blueprint.

        Returns:
            Blueprint with feat placeholders replaced by AI selections.
        """
        # Check if there are any placeholders
        if not any(map(blueprint.feats.__contains__, FeatName.not_choosables())):
            return Blueprint()

        # Build prompt and get AI selection
        prompt = self._build_prompt(blueprint)
        if not prompt:
            return Blueprint()

        structured_llm = self.llm.with_structured_output(FeatSelection)
        _result = structured_llm.invoke(prompt)
        if not isinstance(_result, FeatSelection):
            raise TypeError(f"Expected FeatSelection, got {type(_result)}")
        selection = _result

        # Validate selection count
        count = sum(map(list(blueprint.feats).count, FeatName.not_choosables()))
        if len(selection.feats) != count:
            raise ValueError(
                f"AI returned {len(selection.feats)} feats but expected {count}"
            )

        # Replace placeholders
        new_feats = set(blueprint.feats)
        new_feats.difference_update(FeatName.not_choosables())
        new_feats.update(selection.feats)

        # Count ASI selections and convert to stat choices
        n_ability_score_improvements = sum(
            1 for f in new_feats if f == FeatName.ABILITY_SCORE_IMPROVEMENT
        )

        # Filter out ASI from final feats
        final_feats = tuple(
            f for f in new_feats if f != FeatName.ABILITY_SCORE_IMPROVEMENT
        )

        return Blueprint(
            feats=final_feats, n_stat_choices=2 * n_ability_score_improvements
        )
