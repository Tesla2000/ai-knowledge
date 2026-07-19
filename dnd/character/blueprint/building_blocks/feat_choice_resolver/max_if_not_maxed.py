from typing import Literal

from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)
from dnd.character.blueprint.building_blocks.feat_choice_resolver.base import (
    FeatChoiceResolver,
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

from dnd.character.stats import Stats
from dnd.character.feature.feats import FeatName
from pydantic import Field

_WIK = TypeVar("_WIK", bound=WizardInfo[AnyWizardLevel] | None)
_CK = TypeVar("_CK", bound=CasterInfo | None)


class MaxIfNotMaxedResolver(FeatChoiceResolver):
    """Chooses ASI only if the highest priority stat is not maxed; otherwise no-op."""

    type: Literal[BuildingBlockType.MAX_IF_NOT_MAXED_RESOLVER] = (
        BuildingBlockType.MAX_IF_NOT_MAXED_RESOLVER
    )

    priority: StatsPriority = Field(description="Ability score priority order")

    def _select_from_available(
        self, available: list[FeatName], stats: Stats, stats_cup: Stats
    ) -> FeatName | None:
        highest_priority_stat = self.priority[0]
        if stats.get_stat(highest_priority_stat) < stats_cup.get_stat(
            highest_priority_stat
        ):
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
            return blueprint.model_copy(
                update={
                    "feats": blueprint.feats,
                    "n_stat_choices": blueprint.n_stat_choices,
                }
            )
        return super().apply(blueprint)
