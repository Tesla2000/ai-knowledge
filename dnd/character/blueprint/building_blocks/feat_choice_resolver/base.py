from abc import ABC
from abc import abstractmethod

from typing import TypeVar

from dnd.character.blueprint.building_blocks.building_block import BuildingBlock
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

_WIK = TypeVar("_WIK", bound=WizardInfo[AnyWizardLevel] | None)
_CK = TypeVar("_CK", bound=CasterInfo | None)
from dnd.character.stats import Stats
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
    def _select_from_available(
        self, available: list[FeatName], stats: Stats, stats_cup: Stats
    ) -> FeatName | None: ...

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
        existing_classes = blueprint.classes
        ability_score_improvement_allowed = existing_classes.total_level() != 1

        resolved = set()
        for feat in blueprint.feats:
            result = self._resolve_feat(
                feat,
                blueprint.stats,
                blueprint.stats_cup,
                ability_score_improvement_allowed,
            )
            resolved.add(result if result is not None else feat)

        n_asi = sum(1 for f in resolved if f == FeatName.ABILITY_SCORE_IMPROVEMENT)
        final_feats = tuple(
            f for f in resolved if f != FeatName.ABILITY_SCORE_IMPROVEMENT
        )

        return blueprint.model_copy(
            update={
                "feats": final_feats,
                "n_stat_choices": blueprint.n_stat_choices + 2 * n_asi,
            }
        )

    def _resolve_feat(
        self,
        feat: FeatName,
        stats: Stats,
        stats_cup: Stats,
        ability_score_improvement_allowed: bool,
    ) -> FeatName | None:
        if feat not in FeatName.not_choosables():
            return feat
        excluded = list(FeatName.not_choosables())
        if feat == FeatName.ANY_EXCEPT_ABILITY_SCORE_IMPROVEMENT:
            excluded.append(FeatName.ABILITY_SCORE_IMPROVEMENT)
        if not ability_score_improvement_allowed:
            excluded.append(FeatName.ABILITY_SCORE_IMPROVEMENT)
        available = [f for f in FeatName if f not in excluded]
        return self._select_from_available(available, stats, stats_cup)
