from __future__ import annotations

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
from typing import TypeVar

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
    AnyWizardLevel,
)
from dnd.character.blueprint.states._caster_info import CasterInfo
from dnd.character.blueprint.states.state import Blueprint
from dnd.character.blueprint.states.wizard._info import WizardInfo

from dnd.character.feature.feats import FeatName
from dnd.character.stats import Stats
from dnd.choices.stats_creation.statistic import Statistic
from pydantic import Field

_WIK = TypeVar("_WIK", bound=WizardInfo[AnyWizardLevel] | None)
_CK = TypeVar("_CK", bound=CasterInfo | None)


class MaxFirstResolver(FeatChoiceResolver):
    """Prioritizes maxing stats before choosing other feats.

    When priority is set, tries to max priority[0] first.
    When priority is None (default), tries to max whichever stat currently
    has the highest value that is still below its cap.
    Falls through to `then` when no stat can be increased.
    """

    type: Literal[BuildingBlockType.MAX_FIRST_RESOLVER] = (
        BuildingBlockType.MAX_FIRST_RESOLVER
    )

    priority: StatsPriority | None = Field(default=None)
    then: RandomFeatChoiceResolver = Field(default_factory=RandomFeatChoiceResolver)

    def _select_from_available(
        self, available: list[FeatName], stats: Stats, stats_cup: Stats
    ) -> FeatName | None:
        if FeatName.ABILITY_SCORE_IMPROVEMENT not in available:
            return None
        if self.priority is not None:
            top = self.priority[0]
            if stats.get_stat(top) < stats_cup.get_stat(top):
                return FeatName.ABILITY_SCORE_IMPROVEMENT
            return None
        top = max(Statistic, key=lambda s: stats.get_stat(s))
        if stats.get_stat(top) >= stats_cup.get_stat(top):
            return None
        return FeatName.ABILITY_SCORE_IMPROVEMENT

    def apply(
        self,
        blueprint: Blueprint[
            _RK,
            Stats,
            _HeK,
            _StCK,
            _SkCK,
            _WIK,
            _CK,
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
        _WIK,
        _CK,
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
