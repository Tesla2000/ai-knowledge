from __future__ import annotations

from typing import Literal

from dnd.character.blueprint.building_blocks.abstract_feat_block import (
    AbstractFeatBlock,
)
from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
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
from dnd.character.feature.feats import FeatName
from dnd.character.stats import Stats
from pydantic import Field


class FeatAdder(AbstractFeatBlock):
    """Adds a single concrete feat to the character's feat list."""

    type: Literal[BuildingBlockType.FEAT_ADDER] = BuildingBlockType.FEAT_ADDER

    feat: FeatName = Field(description="Feat to add to character's feat list")

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
        if self.feat in blueprint.feats:
            return blueprint
        return blueprint.model_copy(update={"feats": blueprint.feats + (self.feat,)})
