from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from dnd.character.blueprint.blueprint import Blueprint
from dnd.character.blueprint.building_blocks.building_block import (
    BuildingBlock,
)
from dnd.character.feature.feats import FeatName
from pydantic import ConfigDict


class FeatChoiceResolver(BuildingBlock, ABC):
    """Resolves FeatName.ANY_OF_YOUR_CHOICE placeholders.

    This resolver replaces ANY_OF_YOUR_CHOICE placeholders in the
    blueprint's feats set with concrete FeatName choices.

    Handles special logic for ABILITY_SCORE_IMPROVEMENT:
    - Excluded from choices if character is level 1
    - Converted to n_stat_choices for StatChoiceResolver
    - Filtered out from final feats tuple
    """

    model_config = ConfigDict(frozen=True)

    @abstractmethod
    def select_from_available(
        self, available: list[FeatName], blueprint: Blueprint
    ) -> FeatName:
        """Select a feat from available options.

        Args:
            available: List of FeatName options excluding ANY_OF_YOUR_CHOICE
                      (and possibly ABILITY_SCORE_IMPROVEMENT if level 1).
            blueprint: Current character blueprint for context.

        Returns:
            Selected FeatName.
        """

    def get_change(self, blueprint: Blueprint) -> Blueprint:
        """Replace FeatName.ANY_OF_YOUR_CHOICE placeholders.

        Args:
            blueprint: Current character blueprint.

        Returns:
            Blueprint with feat placeholders replaced and ASI converted
            to n_stat_choices.
        """
        resolved = set()

        # Check if ASI is allowed (level 2+, i.e., total level != 1)
        ability_score_improvement_allowed = sum(blueprint.classes.values()) != 1

        # Build excluded values list
        excluded_values = list(FeatName.not_choosables())
        if not ability_score_improvement_allowed:
            excluded_values.append(FeatName.ABILITY_SCORE_IMPROVEMENT)

        for feat in blueprint.feats:
            resolved.add(self._resolve_feat(feat, blueprint))

        # Count ASI selections and convert to stat choices
        n_ability_score_improvements = sum(
            1 for f in resolved if f == FeatName.ABILITY_SCORE_IMPROVEMENT
        )

        # Filter out ASI from final feats
        final_feats = tuple(
            f for f in resolved if f != FeatName.ABILITY_SCORE_IMPROVEMENT
        )

        return Blueprint(
            feats=final_feats, n_stat_choices=2 * n_ability_score_improvements
        )

    def _resolve_feat(self, feat: FeatName, blueprint: Blueprint):  # type: ignore[no-untyped-def]
        if feat not in FeatName.not_choosables():
            return feat
        available = [f for f in FeatName if f not in FeatName.not_choosables()]
        return self.select_from_available(available, blueprint)
