from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from collections.abc import Generator
from typing import cast
from typing import TYPE_CHECKING

from typing_protocol_intersection import ProtocolIntersection

from dnd.character.blueprint.building_blocks.building_block import BuildingBlock
from dnd.character.blueprint.state import Blueprint
from dnd.character.blueprint.state import BlueprintProtocol
from dnd.character.blueprint.state import HasClasses
from dnd.character.blueprint.state import HasFeats
from dnd.character.blueprint.state import HasNStatChoices
from dnd.character.blueprint.state import HasStats
from dnd.character.class_levels import ClassLevels
from dnd.character.delta.delta import Delta
from dnd.character.feature.feats import FeatName
from pydantic import ConfigDict


class FeatResolutionDelta(Delta):
    """Delta produced when FeatChoiceResolver resolves feat placeholders."""

    feats: tuple[FeatName, ...]
    n_stat_choices: int

    def apply[T: BlueprintProtocol](
        self, state: T
    ) -> ProtocolIntersection[T, HasNStatChoices]:

        if TYPE_CHECKING:

            class BlueprintWithFeatsResolved(Blueprint):
                feats: tuple[FeatName, ...]
                n_stat_choices: int

        else:

            class BlueprintWithFeatsResolved(type(state)):
                feats: tuple[FeatName, ...]
                n_stat_choices: int

        return cast(
            ProtocolIntersection[T, HasNStatChoices],
            BlueprintWithFeatsResolved.model_validate(
                {
                    **dict(state),
                    "feats": self.feats,
                    "n_stat_choices": self.n_stat_choices,
                }
            ),
        )


class FeatChoiceResolver[T: ProtocolIntersection[HasFeats, HasStats]](
    BuildingBlock[T, FeatResolutionDelta, HasNStatChoices], ABC
):
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
    def _select_from_available(
        self, available: list[FeatName], state: T
    ) -> FeatName | None:
        """Select a feat from available options, or None if this resolver cannot choose."""

    def get_change(
        self, state: T
    ) -> Generator[FeatResolutionDelta, None, ProtocolIntersection[T, HasNStatChoices]]:
        existing_classes = (
            state.classes if isinstance(state, HasClasses) else ClassLevels()
        )
        ability_score_improvement_allowed = existing_classes.total_level() != 1

        resolved = set()
        for feat in state.feats:
            result = self._resolve_feat(feat, state, ability_score_improvement_allowed)
            resolved.add(result if result is not None else feat)

        n_asi = sum(1 for f in resolved if f == FeatName.ABILITY_SCORE_IMPROVEMENT)
        final_feats = tuple(
            f for f in resolved if f != FeatName.ABILITY_SCORE_IMPROVEMENT
        )

        delta = FeatResolutionDelta(feats=final_feats, n_stat_choices=2 * n_asi)
        yield delta
        return delta.apply(state)

    def _resolve_feat(
        self, feat: FeatName, state: T, ability_score_improvement_allowed: bool
    ) -> FeatName | None:
        if feat not in FeatName.not_choosables():
            return feat
        excluded = list(FeatName.not_choosables())
        if not ability_score_improvement_allowed:
            excluded.append(FeatName.ABILITY_SCORE_IMPROVEMENT)
        available = [f for f in FeatName if f not in excluded]
        return self._select_from_available(available, state)
