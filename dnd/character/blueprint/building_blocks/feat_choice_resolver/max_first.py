from typing import Literal

from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)
from dnd.character.blueprint.building_blocks.feat_choice_resolver.base import (
    FeatChoiceResolver,
)
from dnd.character.blueprint.building_blocks.feat_choice_resolver.random import (
    RandomFeatChoiceResolver,
)
from dnd.character.blueprint.building_blocks.stats_priority import StatsPriority
from dnd.character.blueprint.sentinels import (
    _ARK,
    _BAK,
    _BDK,
    _CDK,
    _CLK,
    _DRK,
    _FGK,
    _HeK,
    _MOK,
    _PAK,
    _RAK,
    _RK,
    _ROK,
    _SkCK,
    _SOK,
    _StCK,
    _WAK,
    _WZK,
)
from dnd.character.blueprint.states.state import Blueprint
from dnd.character.stats import Stats
from dnd.character.feature.feats import FeatName
from pydantic import Field


class MaxFirstResolver(FeatChoiceResolver):
    """Prioritizes maxing the highest priority stat before choosing other feats."""

    type: Literal[BuildingBlockType.MAX_FIRST_RESOLVER] = (
        BuildingBlockType.MAX_FIRST_RESOLVER
    )

    priority: StatsPriority = Field(description="Ability score priority order")
    then: RandomFeatChoiceResolver = Field(description="Fallback resolver")

    def _select_from_available(
        self, available: list[FeatName], stats: Stats, stats_cup: Stats
    ) -> FeatName | None:
        highest_priority_stat = self.priority[0]
        if FeatName.ABILITY_SCORE_IMPROVEMENT in available and stats.get_stat(
            highest_priority_stat
        ) < stats_cup.get_stat(highest_priority_stat):
            return FeatName.ABILITY_SCORE_IMPROVEMENT
        return None

    def apply(
        self,
        blueprint: Blueprint[
            _RK,
            Stats,
            _HeK,
            _StCK,
            _SkCK,
            _WZK,
            _SOK,
            _FGK,
            _BAK,
            _ROK,
            _CLK,
            _DRK,
            _PAK,
            _RAK,
            _MOK,
            _BDK,
            _WAK,
            _ARK,
            _CDK,
        ],
    ) -> Blueprint[
        _RK,
        Stats,
        _HeK,
        _StCK,
        _SkCK,
        _WZK,
        _SOK,
        _FGK,
        _BAK,
        _ROK,
        _CLK,
        _DRK,
        _PAK,
        _RAK,
        _MOK,
        _BDK,
        _WAK,
        _ARK,
        _CDK,
    ]:
        asi_allowed = blueprint.classes.total_level() != 1
        excluded = [
            *FeatName.not_choosables(),
            *([FeatName.ABILITY_SCORE_IMPROVEMENT] if not asi_allowed else []),
        ]
        available = [f for f in FeatName if f not in excluded]

        if (
            self._select_from_available(available, blueprint.stats, blueprint.stats_cup)
            is None
        ):
            return self.then.apply(blueprint)
        return super().apply(blueprint)
