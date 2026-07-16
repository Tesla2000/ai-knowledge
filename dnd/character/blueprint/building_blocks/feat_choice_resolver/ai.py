"""AI-powered feat choice resolver."""

import json
from dnd.character.blueprint.building_blocks.building_block import BuildingBlock
from dnd.character.blueprint.building_blocks.building_block import _WideBlueprint
from dnd.character.blueprint.states.state import _BPT
from dnd.character.feature.feats import FeatName
from typing import Literal
from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)
from pydantic import BaseModel
from pydantic import Field
from structured_output_creator import OpenAIService, RaisingService


class AIFeatChoiceResolver(BuildingBlock):
    """AI-powered resolver for FeatName.ANY_OF_YOUR_CHOICE placeholders."""

    type: Literal[BuildingBlockType.AI_FEAT_CHOICE_RESOLVER] = (
        BuildingBlockType.AI_FEAT_CHOICE_RESOLVER
    )

    llm: RaisingService[BaseModel] = Field(
        exclude=True, default_factory=lambda: RaisingService(service=OpenAIService())
    )

    def _build_prompt(self, blueprint: _WideBlueprint) -> str:
        system_prompt = (
            "You are resolving FeatName.ANY_OF_YOUR_CHOICE placeholders for a D&D 5e character.\n"
            "Replace each placeholder with the most appropriate feat based on the character's concept.\n"
        )
        character_description = (
            system_prompt
            + "\n\nCharacter state (JSON):\n"
            + json.dumps(
                {
                    k: v
                    for k, v in blueprint.model_dump(mode="json").items()
                    if v is not None
                },
                indent=2,
            )
        )
        count = sum(list(blueprint.feats).count(fc) for fc in FeatName.not_choosables())
        if count == 0:
            return ""
        asi_allowed = blueprint.classes.total_level() != 1
        available_feats = [
            f.value
            for f in FeatName
            if f not in FeatName.not_choosables()
            and (asi_allowed or f != FeatName.ABILITY_SCORE_IMPROVEMENT)
        ]
        asi_note = (
            ""
            if asi_allowed
            else "\nNote: ABILITY_SCORE_IMPROVEMENT is not available at level 1"
        )
        return (
            character_description
            + f"\n## Feats to Choose ({count})\nAvailable: {', '.join(available_feats)}{asi_note}"
        )

    def apply(self, blueprint: _BPT) -> _BPT:
        if not any(map(blueprint.feats.__contains__, FeatName.not_choosables())):
            return blueprint.model_copy(
                update={
                    "feats": blueprint.feats,
                    "n_stat_choices": blueprint.n_stat_choices,
                }
            )

        prompt = self._build_prompt(blueprint)
        if not prompt:
            return blueprint.model_copy(
                update={
                    "feats": blueprint.feats,
                    "n_stat_choices": blueprint.n_stat_choices,
                }
            )

        count = sum(list(blueprint.feats).count(fc) for fc in FeatName.not_choosables())

        class FeatSelection(BaseModel):
            feats: list[FeatName] = Field(min_length=count, max_length=count)

        selection = self.llm.create_structured_output(prompt, FeatSelection)

        new_feats = set(blueprint.feats)
        new_feats.difference_update(FeatName.not_choosables())
        new_feats.update(selection.feats)

        n_asi = sum(1 for f in new_feats if f == FeatName.ABILITY_SCORE_IMPROVEMENT)
        final_feats = tuple(
            f for f in new_feats if f != FeatName.ABILITY_SCORE_IMPROVEMENT
        )

        return blueprint.model_copy(
            update={
                "feats": final_feats,
                "n_stat_choices": blueprint.n_stat_choices + 2 * n_asi,
            }
        )
