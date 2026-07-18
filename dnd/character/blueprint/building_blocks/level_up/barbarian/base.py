from abc import ABC
from abc import abstractmethod
from typing import Literal

from pydantic import Field

from dnd.character.blueprint.building_blocks.building_block import BuildingBlock
from dnd.character.blueprint.building_blocks.feat_block import (
    AnyFeatBlock,
    AnyFeatSelectionBlock,
)
from dnd.character.blueprint.building_blocks.level_up.health_increase import (
    AnyD12HealthIncrease,
    D12HealthIncreaseAverage,
)
from dnd.character.blueprint.sentinels import AnyClassLevel
from dnd.character.blueprint.sentinels import AnySorcererLevel
from dnd.character.blueprint.sentinels import AnyStatChoices
from dnd.character.blueprint.sentinels import AnyWizardLevel
from dnd.character.blueprint.sentinels import ClassPreSubclassLevel
from dnd.character.blueprint.states._caster_info import CasterInfo
from dnd.character.blueprint.states.wizard._info import WizardInfo
from dnd.character.blueprint.sentinels import ClassSubclassLevel
from dnd.character.blueprint.sentinels import MaybeCharacterData
from dnd.character.blueprint.sentinels import MaybeHealth
from dnd.character.blueprint.sentinels import ThirdSubclassPostLevel
from dnd.character.blueprint.sentinels import ThirdSubclassPreLevel
from dnd.character.blueprint.states.barbarian.base import BarbarianBlueprint
from dnd.character.blueprint.states.state import _BPT
from dnd.character.blueprint.states.state import Blueprint
from dnd.character.race.race import Race
from dnd.character.stats import Stats
from dnd.choices.class_creation.character_class import BarbarianSubclass


class BarbarianUpgradeLevelBase[LevelIn: AnyClassLevel, LevelOut: AnyClassLevel](
    BuildingBlock, ABC
):
    """Base for BarbarianLevel1: upgrades Blueprint[Race, Stats, ...] -> BarbarianBlueprint[...]."""

    health_increase: AnyD12HealthIncrease = Field(
        default_factory=D12HealthIncreaseAverage
    )

    @abstractmethod
    def _update_blueprint(self, blueprint: _BPT) -> _BPT: ...

    def apply[
        _HeK_: MaybeHealth,
        _StCK_: AnyStatChoices,
        _SkCK_: AnyStatChoices,
        _WIK_: WizardInfo[AnyWizardLevel] | None,
        _CK_: CasterInfo | None,
        _SOK_: AnySorcererLevel,
        _FGK_: AnyClassLevel,
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
            Race,
            Stats,
            _HeK_,
            _StCK_,
            _SkCK_,
            _WIK_,
            _CK_,
            _SOK_,
            _FGK_,
            LevelIn,
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
    ) -> BarbarianBlueprint[
        _StCK_,
        _SkCK_,
        _WIK_,
        _CK_,
        _SOK_,
        _FGK_,
        LevelOut,
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
        r1 = self._update_blueprint(blueprint)
        r2 = self.health_increase.apply(r1)
        return BarbarianBlueprint[
            _StCK_,
            _SkCK_,
            _WIK_,
            _CK_,
            _SOK_,
            _FGK_,
            LevelOut,
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
        ].model_validate(dict(r2))


class BarbarianPreSubclassLevelBase[
    LevelIn: ThirdSubclassPreLevel,
    LevelOut: ThirdSubclassPreLevel,
](BuildingBlock, ABC):
    """Base for BarbarianLevel2: BarbarianBlueprint[..., ClassPreSubclassLevel[LevelIn, None], ...] -> BarbarianBlueprint[..., ClassPreSubclassLevel[LevelOut, None], ...]."""

    health_increase: AnyD12HealthIncrease = Field(
        default_factory=D12HealthIncreaseAverage
    )

    @abstractmethod
    def _update_blueprint(self, blueprint: _BPT) -> _BPT: ...

    def apply[
        _StCK_: AnyStatChoices,
        _SkCK_: AnyStatChoices,
        _WIK_: WizardInfo[AnyWizardLevel] | None,
        _CK_: CasterInfo | None,
        _SOK_: AnySorcererLevel,
        _FGK_: AnyClassLevel,
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
        blueprint: BarbarianBlueprint[
            _StCK_,
            _SkCK_,
            _WIK_,
            _CK_,
            _SOK_,
            _FGK_,
            ClassPreSubclassLevel[LevelIn, None],
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
    ) -> BarbarianBlueprint[
        _StCK_,
        _SkCK_,
        _WIK_,
        _CK_,
        _SOK_,
        _FGK_,
        ClassPreSubclassLevel[LevelOut, None],
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
        r1 = self._update_blueprint(blueprint)
        r2 = self.health_increase.apply(r1)
        return BarbarianBlueprint[
            _StCK_,
            _SkCK_,
            _WIK_,
            _CK_,
            _SOK_,
            _FGK_,
            ClassPreSubclassLevel[LevelOut, None],
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
        ].model_validate(dict(r2))


class BarbarianSubclassAssignLevelBase[SubclassOut: BarbarianSubclass](
    BuildingBlock, ABC
):
    """Base for BarbarianLevel3*: assigns subclass, ClassPreSubclassLevel[SECOND, None] -> ClassSubclassLevel[THIRD, SubclassOut]."""

    health_increase: AnyD12HealthIncrease = Field(
        default_factory=D12HealthIncreaseAverage
    )

    @abstractmethod
    def _update_blueprint(self, blueprint: _BPT) -> _BPT: ...

    def apply[
        _StCK_: AnyStatChoices,
        _SkCK_: AnyStatChoices,
        _WIK_: WizardInfo[AnyWizardLevel] | None,
        _CK_: CasterInfo | None,
        _SOK_: AnySorcererLevel,
        _FGK_: AnyClassLevel,
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
        blueprint: BarbarianBlueprint[
            _StCK_,
            _SkCK_,
            _WIK_,
            _CK_,
            _SOK_,
            _FGK_,
            ClassPreSubclassLevel[ThirdSubclassPreLevel, None],
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
    ) -> BarbarianBlueprint[
        _StCK_,
        _SkCK_,
        _WIK_,
        _CK_,
        _SOK_,
        _FGK_,
        ClassSubclassLevel[Literal[ThirdSubclassPostLevel.THIRD], SubclassOut],
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
        r1 = self._update_blueprint(blueprint)
        r2 = self.health_increase.apply(r1)
        return BarbarianBlueprint[
            _StCK_,
            _SkCK_,
            _WIK_,
            _CK_,
            _SOK_,
            _FGK_,
            ClassSubclassLevel[Literal[ThirdSubclassPostLevel.THIRD], SubclassOut],
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
        ].model_validate(dict(r2))


class BarbarianSharedLevelBase[
    LevelIn: ThirdSubclassPostLevel,
    LevelOut: ThirdSubclassPostLevel,
](BuildingBlock, ABC):
    """Base for post-subclass barbarian levels shared across all subclasses."""

    health_increase: AnyD12HealthIncrease = Field(
        default_factory=D12HealthIncreaseAverage
    )

    @abstractmethod
    def _update_blueprint(self, blueprint: _BPT) -> _BPT: ...

    def apply[
        SubclassT: BarbarianSubclass,
        _StCK_: AnyStatChoices,
        _SkCK_: AnyStatChoices,
        _WIK_: WizardInfo[AnyWizardLevel] | None,
        _CK_: CasterInfo | None,
        _SOK_: AnySorcererLevel,
        _FGK_: AnyClassLevel,
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
        blueprint: BarbarianBlueprint[
            _StCK_,
            _SkCK_,
            _WIK_,
            _CK_,
            _SOK_,
            _FGK_,
            ClassSubclassLevel[LevelIn, SubclassT],
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
    ) -> BarbarianBlueprint[
        _StCK_,
        _SkCK_,
        _WIK_,
        _CK_,
        _SOK_,
        _FGK_,
        ClassSubclassLevel[LevelOut, SubclassT],
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
        r1 = self._update_blueprint(blueprint)
        r2 = self.health_increase.apply(r1)
        return BarbarianBlueprint[
            _StCK_,
            _SkCK_,
            _WIK_,
            _CK_,
            _SOK_,
            _FGK_,
            ClassSubclassLevel[LevelOut, SubclassT],
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
        ].model_validate(dict(r2))


class BarbarianFeatGrantingLevelBase[
    LevelIn: ThirdSubclassPostLevel,
    LevelOut: ThirdSubclassPostLevel,
](BarbarianSharedLevelBase[LevelIn, LevelOut]):
    """Base for barbarian levels that grant a feat choice (4, 8, 12, 16, 19)."""

    feat_block: AnyFeatBlock = Field(default_factory=AnyFeatSelectionBlock)

    def apply[
        SubclassT: BarbarianSubclass,
        _StCK_: AnyStatChoices,
        _SkCK_: AnyStatChoices,
        _WIK_: WizardInfo[AnyWizardLevel] | None,
        _CK_: CasterInfo | None,
        _SOK_: AnySorcererLevel,
        _FGK_: AnyClassLevel,
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
        blueprint: BarbarianBlueprint[
            _StCK_,
            _SkCK_,
            _WIK_,
            _CK_,
            _SOK_,
            _FGK_,
            ClassSubclassLevel[LevelIn, SubclassT],
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
    ) -> BarbarianBlueprint[
        _StCK_,
        _SkCK_,
        _WIK_,
        _CK_,
        _SOK_,
        _FGK_,
        ClassSubclassLevel[LevelOut, SubclassT],
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
        result = super().apply(blueprint)
        feat_applied = self.feat_block.apply(result)
        return result.model_copy(
            update={
                "feats": feat_applied.feats,
                "stats": feat_applied.stats,
                "n_stat_choices": feat_applied.n_stat_choices,
            }
        )


class BarbarianSubclassFeatureLevelBase[
    LevelIn: AnyClassLevel,
    LevelOut: AnyClassLevel,
](BuildingBlock, ABC):
    """Base for barbarian levels 6, 10, 14 that grant subclass-specific features."""

    health_increase: AnyD12HealthIncrease = Field(
        default_factory=D12HealthIncreaseAverage
    )

    @abstractmethod
    def _update_blueprint(self, blueprint: _BPT) -> _BPT: ...

    def apply[
        _StCK_: AnyStatChoices,
        _SkCK_: AnyStatChoices,
        _WIK_: WizardInfo[AnyWizardLevel] | None,
        _CK_: CasterInfo | None,
        _SOK_: AnySorcererLevel,
        _FGK_: AnyClassLevel,
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
        blueprint: BarbarianBlueprint[
            _StCK_,
            _SkCK_,
            _WIK_,
            _CK_,
            _SOK_,
            _FGK_,
            LevelIn,
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
    ) -> BarbarianBlueprint[
        _StCK_,
        _SkCK_,
        _WIK_,
        _CK_,
        _SOK_,
        _FGK_,
        LevelOut,
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
        r1 = self._update_blueprint(blueprint)
        r2 = self.health_increase.apply(r1)
        return BarbarianBlueprint[
            _StCK_,
            _SkCK_,
            _WIK_,
            _CK_,
            _SOK_,
            _FGK_,
            LevelOut,
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
        ].model_validate(dict(r2))
