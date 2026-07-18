from __future__ import annotations

from typing import Literal

from pydantic import Field

from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)
from dnd.character.blueprint.building_blocks.feat_block.base import AbstractFeatBlock
from dnd.character.blueprint.building_blocks.stat_choice_resolver import (
    AnyStatChoiceResolver,
)
from dnd.character.blueprint.building_blocks.stat_choice_resolver.max import (
    MaxStatChoiceResolver,
)
from dnd.character.blueprint.sentinels import (
    AnyClassLevel,
    AnySorcererLevel,
    AnyStatChoices,
    AnyWizardLevel,
    MaybeCharacterData,
    MaybeHealth,
    MaybeRace,
)
from dnd.character.blueprint.states._caster_info import CasterInfo
from dnd.character.blueprint.states.state import Blueprint
from dnd.character.blueprint.states.wizard._info import WizardInfo
from dnd.character.stats import Stats


class AbilityScoreImprovementFeatBlock(AbstractFeatBlock):
    """Grants +2 stat choices and immediately resolves them via stat_resolver."""

    type: Literal[BuildingBlockType.ABILITY_SCORE_IMPROVEMENT_FEAT_BLOCK] = (
        BuildingBlockType.ABILITY_SCORE_IMPROVEMENT_FEAT_BLOCK
    )
    stat_resolver: AnyStatChoiceResolver = Field(default_factory=MaxStatChoiceResolver)

    def apply[
        _RK_: MaybeRace,
        _HeK_: MaybeHealth,
        _StCK_: AnyStatChoices,
        _SkCK_: AnyStatChoices,
        _WIK_: WizardInfo[AnyWizardLevel] | None,
        _CK_: CasterInfo | None,
        _SOK_: AnySorcererLevel,
        _FGK_: AnyClassLevel,
        _BAK_: AnyClassLevel,
        _ROK_: AnyClassLevel,
        _CLK_: AnyClassLevel,
        _DRK_: AnyClassLevel,
        _PAK_: AnyClassLevel,
        _RAK_: AnyClassLevel,
        _MOK_: AnyClassLevel,
        _BDK_: AnyClassLevel,
        _WAK_: AnyClassLevel,
        _ARK_: AnyClassLevel,
        _CDK_: MaybeCharacterData,
    ](
        self,
        blueprint: Blueprint[
            _RK_,
            Stats,
            _HeK_,
            _StCK_,
            _SkCK_,
            _WIK_,
            _CK_,
            _SOK_,
            _FGK_,
            _BAK_,
            _ROK_,
            _CLK_,
            _DRK_,
            _PAK_,
            _RAK_,
            _MOK_,
            _BDK_,
            _WAK_,
            _ARK_,
            _CDK_,
        ],
    ) -> Blueprint[
        _RK_,
        Stats,
        _HeK_,
        _StCK_,
        _SkCK_,
        _WIK_,
        _CK_,
        _SOK_,
        _FGK_,
        _BAK_,
        _ROK_,
        _CLK_,
        _DRK_,
        _PAK_,
        _RAK_,
        _MOK_,
        _BDK_,
        _WAK_,
        _ARK_,
        _CDK_,
    ]:
        with_choices = blueprint.model_copy(
            update={"n_stat_choices": blueprint.n_stat_choices + 2}
        )
        stat_applied = self.stat_resolver.apply(with_choices)
        return blueprint.model_copy(
            update={
                "stats": stat_applied.stats,
                "n_stat_choices": stat_applied.n_stat_choices,
            }
        )
