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
    AnyD6HealthIncrease,
    D6HealthIncreaseAverage,
)
from dnd.character.blueprint.building_blocks.level_up.spell_assignment import (
    AnySorcererSpellAssigner,
    SorcererRandomSpellAssigner,
)
from dnd.character.blueprint.sentinels import AnyClassLevel
from dnd.character.blueprint.sentinels import AnyMetamagicChoices
from dnd.character.blueprint.sentinels import AnyNonZeroSorcererLevel
from dnd.character.blueprint.sentinels import AnyStatChoices
from dnd.character.blueprint.sentinels import AnyWizardLevel
from dnd.character.blueprint.states._caster_info import CasterInfo
from dnd.character.blueprint.states.wizard._info import WizardInfo
from dnd.character.blueprint.sentinels import FirstSubclassPostLevel
from dnd.character.blueprint.sentinels import FirstSubclassPreLevel
from dnd.character.blueprint.sentinels import MaybeCharacterData
from dnd.character.blueprint.sentinels import MaybeHealth
from dnd.character.blueprint.sentinels import SorcererPreSubclassLevel
from dnd.character.blueprint.sentinels import SorcererSubclassLevel
from dnd.character.blueprint.states.sorcerer.base import SorcererBlueprint
from dnd.character.blueprint.states.sorcerer.base import _SBPT
from dnd.character.blueprint.states.state import Blueprint
from dnd.character.blueprint.states.state import _BPT
from dnd.character.race.race import Race
from dnd.character.spells.max_spell_levels import FULL_CASTER_SPELL_SLOTS
from dnd.character.stats import Stats
from dnd.choices.class_creation.character_class import SorcererSubclass


class SorcererLevel1Base[SubclassOut: SorcererSubclass](BuildingBlock, ABC):
    """Base for sorcerer level 1 (subclass-assigning level)."""

    health_increase: AnyD6HealthIncrease = Field(
        default_factory=D6HealthIncreaseAverage
    )
    spell_assigner: AnySorcererSpellAssigner = Field(
        default_factory=SorcererRandomSpellAssigner
    )

    @abstractmethod
    def _update_blueprint(self, blueprint: _BPT) -> _BPT: ...

    def apply[
        _HeK_: MaybeHealth,
        _StCK_: AnyStatChoices,
        _SkCK_: AnyStatChoices,
        _WIK_: WizardInfo[AnyWizardLevel] | None,
        _CK_: CasterInfo | None,
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
            Race,
            Stats,
            _HeK_,
            _StCK_,
            _SkCK_,
            _WIK_,
            _CK_,
            SorcererPreSubclassLevel[FirstSubclassPreLevel, None],
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
    ) -> SorcererBlueprint[
        _StCK_,
        _SkCK_,
        _WIK_,
        _CK_,
        SorcererSubclassLevel[Literal[FirstSubclassPostLevel.FIRST], SubclassOut],
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
        Literal[0],
    ]:
        r1 = self._update_blueprint(blueprint)
        r2 = self.health_increase.apply(r1)
        sorc_r2 = SorcererBlueprint[
            _StCK_,
            _SkCK_,
            _WIK_,
            _CK_,
            SorcererSubclassLevel[Literal[FirstSubclassPostLevel.FIRST], SubclassOut],
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
            Literal[0],
        ].model_validate(
            dict(r2)
            | {"spell_slots": FULL_CASTER_SPELL_SLOTS[0], "n_metamagic_choices": 0}
        )
        r3 = self.spell_assigner.apply(sorc_r2)
        return r3.increase_full_caster()


class SorcererSharedLevelBase[
    LevelIn: FirstSubclassPostLevel,
    LevelOut: FirstSubclassPostLevel,
](BuildingBlock, ABC):
    """Base for post-subclass sorcerer levels shared across all subclasses."""

    health_increase: AnyD6HealthIncrease = Field(
        default_factory=D6HealthIncreaseAverage
    )
    spell_assigner: AnySorcererSpellAssigner = Field(
        default_factory=SorcererRandomSpellAssigner
    )

    @abstractmethod
    def _update_blueprint(self, blueprint: _SBPT) -> _SBPT: ...

    def apply[
        SubclassT: SorcererSubclass,
        _StCK_: AnyStatChoices,
        _SkCK_: AnyStatChoices,
        _WIK_: WizardInfo[AnyWizardLevel] | None,
        _CK_: CasterInfo | None,
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
        _McK_: AnyMetamagicChoices,
    ](
        self,
        blueprint: SorcererBlueprint[
            _StCK_,
            _SkCK_,
            _WIK_,
            _CK_,
            SorcererSubclassLevel[LevelIn, SubclassT],
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
            _McK_,
        ],
    ) -> SorcererBlueprint[
        _StCK_,
        _SkCK_,
        _WIK_,
        _CK_,
        SorcererSubclassLevel[LevelOut, SubclassT],
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
        _McK_,
    ]:
        r1 = self._update_blueprint(blueprint)
        r2 = self.health_increase.apply(r1)
        sorc_r2 = SorcererBlueprint[
            _StCK_,
            _SkCK_,
            _WIK_,
            _CK_,
            SorcererSubclassLevel[LevelOut, SubclassT],
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
            _McK_,
        ].model_validate(
            dict(r2)
            | {
                "spell_slots": blueprint.spell_slots,
                "caster_level": blueprint.caster_level,
                "n_metamagic_choices": blueprint.n_metamagic_choices,
            }
        )
        r3 = self.spell_assigner.apply(sorc_r2)
        return r3.increase_full_caster()


class SorcererFeatGrantingLevelBase[
    LevelIn: FirstSubclassPostLevel,
    LevelOut: FirstSubclassPostLevel,
](SorcererSharedLevelBase[LevelIn, LevelOut]):
    """Base for sorcerer levels that grant a feat choice (4, 8, 12, 16, 19)."""

    feat_block: AnyFeatBlock = Field(default_factory=AnyFeatSelectionBlock)

    def apply[
        SubclassT: SorcererSubclass,
        _StCK_: AnyStatChoices,
        _SkCK_: AnyStatChoices,
        _WIK_: WizardInfo[AnyWizardLevel] | None,
        _CK_: CasterInfo | None,
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
        _McK_: AnyMetamagicChoices,
    ](
        self,
        blueprint: SorcererBlueprint[
            _StCK_,
            _SkCK_,
            _WIK_,
            _CK_,
            SorcererSubclassLevel[LevelIn, SubclassT],
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
            _McK_,
        ],
    ) -> SorcererBlueprint[
        _StCK_,
        _SkCK_,
        _WIK_,
        _CK_,
        SorcererSubclassLevel[LevelOut, SubclassT],
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
        _McK_,
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


class SorcererSubclassFeatureLevelBase[
    LevelIn: AnyNonZeroSorcererLevel,
    LevelOut: AnyNonZeroSorcererLevel,
](BuildingBlock, ABC):
    """Base for sorcerer levels 6, 14, 18 that grant subclass-specific features."""

    health_increase: AnyD6HealthIncrease = Field(
        default_factory=D6HealthIncreaseAverage
    )
    spell_assigner: AnySorcererSpellAssigner = Field(
        default_factory=SorcererRandomSpellAssigner
    )

    @abstractmethod
    def _update_blueprint(self, blueprint: _BPT) -> _BPT: ...

    def apply[
        _StCK_: AnyStatChoices,
        _SkCK_: AnyStatChoices,
        _WIK_: WizardInfo[AnyWizardLevel] | None,
        _CK_: CasterInfo | None,
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
        _McK_: AnyMetamagicChoices,
    ](
        self,
        blueprint: SorcererBlueprint[
            _StCK_,
            _SkCK_,
            _WIK_,
            _CK_,
            LevelIn,
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
            _McK_,
        ],
    ) -> SorcererBlueprint[
        _StCK_,
        _SkCK_,
        _WIK_,
        _CK_,
        LevelOut,
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
        _McK_,
    ]:
        r1 = self._update_blueprint(blueprint)
        r2 = self.health_increase.apply(r1)
        sorc_r2 = SorcererBlueprint[
            _StCK_,
            _SkCK_,
            _WIK_,
            _CK_,
            LevelOut,
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
            _McK_,
        ].model_validate(
            dict(r2)
            | {
                "spell_slots": blueprint.spell_slots,
                "caster_level": blueprint.caster_level,
                "n_metamagic_choices": blueprint.n_metamagic_choices,
            }
        )
        r3 = self.spell_assigner.apply(sorc_r2)
        return r3.increase_full_caster()
