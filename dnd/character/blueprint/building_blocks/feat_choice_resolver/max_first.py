from __future__ import annotations

from collections.abc import Generator
from typing import Literal
from typing import overload
from typing import Protocol
from typing import runtime_checkable

from typing_extensions import deprecated
from typing_protocol_intersection import ProtocolIntersection

from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)
from dnd.character.blueprint.building_blocks.feat_choice_resolver.base import (
    FeatChoiceResolver,
    FeatResolutionDelta,
    _FeatT,
)
from dnd.character.blueprint.building_blocks.feat_choice_resolver.random import (
    RandomFeatChoiceResolver,
)
from dnd.character.blueprint.building_blocks.stats_priority import StatsPriority
from dnd.character.blueprint.state import BlueprintProtocol
from dnd.character.blueprint.state import HasClasses
from dnd.character.blueprint.state import HasNStatChoices
from dnd.character.blueprint.state import HasStatsCup
from dnd.character.class_levels import ClassLevels
from dnd.character.delta.delta import Delta
from dnd.character.feature.feats import FeatName
from pydantic import Field


@runtime_checkable
class _MaxFeatT(_FeatT, HasStatsCup, Protocol):
    pass


class MaxFirstResolver(FeatChoiceResolver[_MaxFeatT]):
    """Prioritizes maxing the highest priority stat before choosing other feats.

    Checks if the highest priority stat is below its cap and selects Ability Score
    Improvement if so. Otherwise, delegates to the fallback resolver.

    Returns None from _select_from_available when ASI is not available or the stat is
    already maxed; get_change catches this and falls back to then.

    Example:
        >>> resolver = MaxFirstResolver(
        ...     priority=StatsPriority((Statistic.STR, ...)),
        ...     then=RandomFeatChoiceResolver()
        ... )
        >>> # Will choose ASI if STR < cap, otherwise random feat
    """

    type: Literal[BuildingBlockType.MAX_FIRST_RESOLVER] = (
        BuildingBlockType.MAX_FIRST_RESOLVER
    )

    priority: StatsPriority = Field(
        description="Ability score priority order for determining which stat to max"
    )
    then: RandomFeatChoiceResolver = Field(
        description="Fallback resolver to use when highest priority stat is already maxed"
    )

    def _select_from_available(
        self, available: list[FeatName], state: _MaxFeatT
    ) -> FeatName | None:
        highest_priority_stat = self.priority[0]
        if FeatName.ABILITY_SCORE_IMPROVEMENT in available and state.stats.get_stat(
            highest_priority_stat
        ) < state.stats_cup.get_stat(highest_priority_stat):
            return FeatName.ABILITY_SCORE_IMPROVEMENT
        return None

    @overload
    def get_change[T: _FeatT](
        self, state: T
    ) -> Generator[
        FeatResolutionDelta, None, ProtocolIntersection[T, HasNStatChoices]
    ]: ...

    @overload
    @deprecated(
        "Pass a state satisfying HasFeats and HasStats for precise return typing"
    )
    def get_change[T: BlueprintProtocol](
        self, state: T
    ) -> Generator[Delta, None, BlueprintProtocol]: ...

    def get_change[T: BlueprintProtocol](
        self, state: T
    ) -> Generator[Delta, None, BlueprintProtocol]:
        if not isinstance(state, _MaxFeatT):
            raise TypeError(
                f"{type(self).__name__} requires HasFeats, HasStats and HasStatsCup, got {type(state).__name__}"
            )
        existing_classes = (
            state.classes if isinstance(state, HasClasses) else ClassLevels()
        )
        asi_allowed = existing_classes.total_level() != 1
        excluded = [
            *FeatName.not_choosables(),
            *([FeatName.ABILITY_SCORE_IMPROVEMENT] if not asi_allowed else []),
        ]
        available = [f for f in FeatName if f not in excluded]

        if self._select_from_available(available, state) is None:
            return (yield from self.then.get_change(state))
        return (yield from super().get_change(state))
