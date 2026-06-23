"""AI-powered feat choice resolver."""

from __future__ import annotations

from collections.abc import Generator

from typing_protocol_intersection import ProtocolIntersection

from dnd.character.blueprint.blueprint_formatter import BlueprintFormatter
from dnd.character.blueprint.building_blocks.building_block import BuildingBlock
from dnd.character.blueprint.building_blocks.feat_choice_resolver.base import (
    FeatResolutionDelta,
)
from dnd.character.blueprint.state import HasClasses
from dnd.character.blueprint.state import HasFeats
from dnd.character.blueprint.state import HasNStatChoices
from dnd.character.blueprint.state import HasStats
from dnd.character.feature.feats import FeatName
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from pydantic import Field


class FeatSelection(BaseModel):
    """Schema for AI to select feat replacements."""

    feats: set[FeatName] = Field(default_factory=set)


class AIFeatChoiceResolver[
    T: ProtocolIntersection[ProtocolIntersection[HasFeats, HasStats], HasClasses]
](BuildingBlock[T, FeatResolutionDelta, HasNStatChoices]):
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

    def _build_prompt(self, state: T) -> str:
        system_prompt = (
            "You are resolving FeatName.ANY_OF_YOUR_CHOICE placeholders "
            "for a D&D 5e character.\n"
            "Replace each placeholder with the most appropriate feat "
            "based on the character's race, class, stats, and concept.\n"
        )

        character_description = self.formatter.format(
            state, system_prompt=system_prompt
        )

        instructions = ["\n## Placeholders to Resolve\n"]

        feat_list = list(state.feats)
        count = sum(feat_list.count(fc) for fc in FeatName.not_choosables())
        if count == 0:
            return ""

        instructions.append(
            f"Feats: {count} ANY_OF_YOUR_CHOICE placeholder(s) to replace"
        )

        ability_score_improvement_allowed = state.classes.total_level() != 1

        available_feats = [
            f.value
            for f in FeatName
            if f not in FeatName.not_choosables()
            and (
                ability_score_improvement_allowed
                or f != FeatName.ABILITY_SCORE_IMPROVEMENT
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

    def get_change(
        self, state: T
    ) -> Generator[FeatResolutionDelta, None, ProtocolIntersection[T, HasNStatChoices]]:
        if not any(map(state.feats.__contains__, FeatName.not_choosables())):
            delta = FeatResolutionDelta(feats=state.feats, n_stat_choices=0)
            yield delta
            return delta.apply(state)

        prompt = self._build_prompt(state)
        if not prompt:
            delta = FeatResolutionDelta(feats=state.feats, n_stat_choices=0)
            yield delta
            return delta.apply(state)

        structured_llm = self.llm.with_structured_output(FeatSelection)
        _result = structured_llm.invoke(prompt)
        if not isinstance(_result, FeatSelection):
            raise TypeError(f"Expected FeatSelection, got {type(_result)}")
        selection = _result

        feat_list = list(state.feats)
        count = sum(feat_list.count(fc) for fc in FeatName.not_choosables())
        if len(selection.feats) != count:
            raise ValueError(
                f"AI returned {len(selection.feats)} feats but expected {count}"
            )

        new_feats = set(state.feats)
        new_feats.difference_update(FeatName.not_choosables())
        new_feats.update(selection.feats)

        n_asi = sum(1 for f in new_feats if f == FeatName.ABILITY_SCORE_IMPROVEMENT)
        final_feats = tuple(
            f for f in new_feats if f != FeatName.ABILITY_SCORE_IMPROVEMENT
        )

        delta = FeatResolutionDelta(feats=final_feats, n_stat_choices=2 * n_asi)
        yield delta
        return delta.apply(state)
