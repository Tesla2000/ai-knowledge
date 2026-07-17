from abc import ABC
from abc import abstractmethod

from pydantic import Field

from dnd.character.blueprint.building_blocks.building_block import BuildingBlock
from dnd.character.blueprint.building_blocks.level_up.health_increase import (
    AnyD6HealthIncrease,
    D6HealthIncreaseAverage,
)
from dnd.character.blueprint.building_blocks.feat_block import (
    AnyFeatBlock,
    AnyFeatSelectionBlock,
)
from dnd.character.blueprint.building_blocks.level_up.spell_assignment import (
    AnyWizardSpellAssigner,
    WizardRandomSpellAssigner,
)
from dnd.character.blueprint.sentinels import AnyClassLevel
from dnd.character.blueprint.sentinels import AnyNonZeroWizardLevel
from dnd.character.blueprint.sentinels import AnySorcererLevel
from dnd.character.blueprint.sentinels import AnyStatChoices
from dnd.character.blueprint.sentinels import AnyWizardLevel
from dnd.character.blueprint.sentinels import MaybeCharacterData
from dnd.character.blueprint.sentinels import MaybeHealth
from dnd.character.blueprint.sentinels import SecondSubclassPostLevel
from dnd.character.blueprint.sentinels import WizardSubclassLevel
from pydantic import PositiveInt
from dnd.character.blueprint.states.state import Blueprint
from dnd.character.blueprint.states.state import _BPT
from dnd.character.blueprint.states.wizard.base import WizardBlueprint
from dnd.character.blueprint.states.wizard.level18 import WizardLevel18Blueprint
from dnd.character.blueprint.states.wizard.level20 import WizardLevel20Blueprint
from dnd.character.race.race import Race
from dnd.character.spells.max_spell_levels import FULL_CASTER_SPELL_SLOTS
from dnd.character.stats import Stats
from dnd.choices.class_creation.character_class import WizardSubclass


class WizardUpgradeLevelBase[LevelIn: AnyWizardLevel, LevelOut: AnyNonZeroWizardLevel](
    BuildingBlock, ABC
):
    """Base for WizardLevel1: upgrades Blueprint[Race, Stats, ...] → WizardBlueprint[...]."""

    health_increase: AnyD6HealthIncrease = Field(
        default_factory=D6HealthIncreaseAverage
    )
    spell_assigner: AnyWizardSpellAssigner = Field(
        default_factory=WizardRandomSpellAssigner
    )

    @abstractmethod
    def _update_blueprint(self, blueprint: _BPT) -> _BPT: ...

    def apply[
        _HeK_: MaybeHealth,
        _StCK_: AnyStatChoices,
        _SkCK_: AnyStatChoices,
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
            Race,
            Stats,
            _HeK_,
            _StCK_,
            _SkCK_,
            LevelIn,
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
    ) -> WizardBlueprint[
        _StCK_,
        _SkCK_,
        LevelOut,
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
        r1 = self._update_blueprint(blueprint)
        r2 = self.health_increase.apply(r1)
        wiz_r2 = WizardBlueprint[
            _StCK_,
            _SkCK_,
            LevelOut,
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
        ].model_validate(dict(r2) | {"spell_slots": FULL_CASTER_SPELL_SLOTS[0]})
        r3 = self.spell_assigner.apply(wiz_r2)
        return r3.increase_full_caster()


class WizardPreSubclassLevelBase[
    LevelIn: AnyNonZeroWizardLevel,
    LevelOut: AnyNonZeroWizardLevel,
](BuildingBlock, ABC):
    """Base for WizardLevel2*: WizardBlueprint[..., LevelIn, ...] → WizardBlueprint[..., LevelOut, ...]."""

    health_increase: AnyD6HealthIncrease = Field(
        default_factory=D6HealthIncreaseAverage
    )
    spell_assigner: AnyWizardSpellAssigner = Field(
        default_factory=WizardRandomSpellAssigner
    )

    @abstractmethod
    def _update_blueprint(self, blueprint: _BPT) -> _BPT: ...

    def apply[
        _StCK_: AnyStatChoices,
        _SkCK_: AnyStatChoices,
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
        blueprint: WizardBlueprint[
            _StCK_,
            _SkCK_,
            LevelIn,
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
    ) -> WizardBlueprint[
        _StCK_,
        _SkCK_,
        LevelOut,
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
        r1 = self._update_blueprint(blueprint)
        r2 = self.health_increase.apply(r1)
        wiz_r2 = WizardBlueprint[
            _StCK_,
            _SkCK_,
            LevelOut,
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
        ].model_validate(
            dict(r2)
            | {
                "prepared_spells": blueprint.prepared_spells,
                "spell_slots": blueprint.spell_slots,
                "caster_level": blueprint.caster_level,
            }
        )
        r3 = self.spell_assigner.apply(wiz_r2)
        return r3.increase_full_caster()


class WizardSharedLevelBase[
    LevelIn: SecondSubclassPostLevel,
    LevelOut: SecondSubclassPostLevel,
](BuildingBlock, ABC):
    """Base for post-subclass wizard levels (3–20) shared across all subclasses."""

    health_increase: AnyD6HealthIncrease = Field(
        default_factory=D6HealthIncreaseAverage
    )
    spell_assigner: AnyWizardSpellAssigner = Field(
        default_factory=WizardRandomSpellAssigner
    )

    @abstractmethod
    def _update_blueprint(self, blueprint: _BPT) -> _BPT: ...

    def apply[
        SubclassT: WizardSubclass,
        _StCK_: AnyStatChoices,
        _SkCK_: AnyStatChoices,
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
        blueprint: WizardBlueprint[
            _StCK_,
            _SkCK_,
            WizardSubclassLevel[LevelIn, SubclassT],
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
    ) -> WizardBlueprint[
        _StCK_,
        _SkCK_,
        WizardSubclassLevel[LevelOut, SubclassT],
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
        r1 = self._update_blueprint(blueprint)
        r2 = self.health_increase.apply(r1)
        wiz_r2 = WizardBlueprint[
            _StCK_,
            _SkCK_,
            WizardSubclassLevel[LevelOut, SubclassT],
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
        ].model_validate(
            dict(r2)
            | {
                "prepared_spells": blueprint.prepared_spells,
                "spell_slots": blueprint.spell_slots,
                "caster_level": blueprint.caster_level,
            }
        )
        r3 = self.spell_assigner.apply(wiz_r2)
        return r3.increase_full_caster()


class WizardFeatGrantingLevelBase[
    LevelIn: SecondSubclassPostLevel,
    LevelOut: SecondSubclassPostLevel,
](WizardSharedLevelBase[LevelIn, LevelOut]):
    """Base for wizard levels that grant a feat choice (4, 8, 12, 16, 19)."""

    feat_block: AnyFeatBlock = Field(default_factory=AnyFeatSelectionBlock)

    def apply[
        SubclassT: WizardSubclass,
        _StCK_: AnyStatChoices,
        _SkCK_: AnyStatChoices,
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
        blueprint: WizardBlueprint[
            _StCK_,
            _SkCK_,
            WizardSubclassLevel[LevelIn, SubclassT],
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
    ) -> WizardBlueprint[
        _StCK_,
        _SkCK_,
        WizardSubclassLevel[LevelOut, SubclassT],
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
        result = super().apply(blueprint)
        feat_applied = self.feat_block.apply(result)
        return result.model_copy(
            update={
                "feats": feat_applied.feats,
                "stats": feat_applied.stats,
                "n_stat_choices": feat_applied.n_stat_choices,
            }
        )


class WizardLevel18UpgradeLevelBase[
    LevelIn: SecondSubclassPostLevel,
    LevelOut: SecondSubclassPostLevel,
](BuildingBlock, ABC):
    """Base for WizardLevel18: WizardBlueprint → WizardLevel18Blueprint."""

    health_increase: AnyD6HealthIncrease = Field(
        default_factory=D6HealthIncreaseAverage
    )
    spell_assigner: AnyWizardSpellAssigner = Field(
        default_factory=WizardRandomSpellAssigner
    )

    @abstractmethod
    def _update_blueprint(self, blueprint: _BPT) -> _BPT: ...

    def apply[
        SubclassT: WizardSubclass,
        _StCK_: AnyStatChoices,
        _SkCK_: AnyStatChoices,
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
        blueprint: WizardBlueprint[
            _StCK_,
            _SkCK_,
            WizardSubclassLevel[LevelIn, SubclassT],
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
    ) -> WizardLevel18Blueprint[
        _StCK_,
        _SkCK_,
        WizardSubclassLevel[LevelOut, SubclassT],
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
        r1 = self._update_blueprint(blueprint)
        r2 = self.health_increase.apply(r1)
        wiz_r2 = WizardBlueprint[
            _StCK_,
            _SkCK_,
            WizardSubclassLevel[LevelOut, SubclassT],
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
        ].model_validate(
            dict(r2)
            | {
                "prepared_spells": blueprint.prepared_spells,
                "spell_slots": blueprint.spell_slots,
                "caster_level": blueprint.caster_level,
            }
        )
        r3 = self.spell_assigner.apply(wiz_r2)
        partial = WizardLevel18Blueprint[
            _StCK_,
            _SkCK_,
            WizardSubclassLevel[LevelOut, SubclassT],
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
        ].model_validate(dict(r3) | {"spell_mastery_spells": ()})
        return partial.increase_full_caster()


class WizardPostLevel18SharedLevelBase[
    LevelIn: SecondSubclassPostLevel,
    LevelOut: SecondSubclassPostLevel,
](BuildingBlock, ABC):
    """Base for WizardLevel19: WizardLevel18Blueprint → WizardLevel18Blueprint."""

    health_increase: AnyD6HealthIncrease = Field(
        default_factory=D6HealthIncreaseAverage
    )
    spell_assigner: AnyWizardSpellAssigner = Field(
        default_factory=WizardRandomSpellAssigner
    )

    @abstractmethod
    def _update_blueprint(self, blueprint: _BPT) -> _BPT: ...

    def apply[
        SubclassT: WizardSubclass,
        _StCK_: AnyStatChoices,
        _SkCK_: AnyStatChoices,
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
        blueprint: WizardLevel18Blueprint[
            _StCK_,
            _SkCK_,
            WizardSubclassLevel[LevelIn, SubclassT],
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
    ) -> WizardLevel18Blueprint[
        _StCK_,
        _SkCK_,
        WizardSubclassLevel[LevelOut, SubclassT],
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
        r1 = self._update_blueprint(blueprint)
        r2 = self.health_increase.apply(r1)
        wiz_r2 = WizardBlueprint[
            _StCK_,
            _SkCK_,
            WizardSubclassLevel[LevelOut, SubclassT],
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
        ].model_validate(
            dict(r2)
            | {
                "prepared_spells": blueprint.prepared_spells,
                "spell_slots": blueprint.spell_slots,
                "caster_level": blueprint.caster_level,
            }
        )
        r3 = self.spell_assigner.apply(wiz_r2)
        partial = WizardLevel18Blueprint[
            _StCK_,
            _SkCK_,
            WizardSubclassLevel[LevelOut, SubclassT],
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
        ].model_validate(
            dict(r3) | {"spell_mastery_spells": blueprint.spell_mastery_spells}
        )
        return partial.increase_full_caster()


class WizardPostLevel18FeatGrantingLevelBase[
    LevelIn: SecondSubclassPostLevel,
    LevelOut: SecondSubclassPostLevel,
](WizardPostLevel18SharedLevelBase[LevelIn, LevelOut]):
    """Base for wizard level 19 which grants a feat choice."""

    feat_block: AnyFeatBlock = Field(default_factory=AnyFeatSelectionBlock)

    def apply[
        SubclassT: WizardSubclass,
        _StCK_: AnyStatChoices,
        _SkCK_: AnyStatChoices,
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
        blueprint: WizardLevel18Blueprint[
            _StCK_,
            _SkCK_,
            WizardSubclassLevel[LevelIn, SubclassT],
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
    ) -> WizardLevel18Blueprint[
        _StCK_,
        _SkCK_,
        WizardSubclassLevel[LevelOut, SubclassT],
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
        result = super().apply(blueprint)
        feat_applied = self.feat_block.apply(result)
        return result.model_copy(
            update={
                "feats": feat_applied.feats,
                "stats": feat_applied.stats,
                "n_stat_choices": feat_applied.n_stat_choices,
            }
        )


class WizardLevel20UpgradeLevelBase[
    LevelIn: SecondSubclassPostLevel,
    LevelOut: SecondSubclassPostLevel,
](BuildingBlock, ABC):
    """Base for WizardLevel20: WizardLevel18Blueprint → WizardLevel20Blueprint."""

    health_increase: AnyD6HealthIncrease = Field(
        default_factory=D6HealthIncreaseAverage
    )
    spell_assigner: AnyWizardSpellAssigner = Field(
        default_factory=WizardRandomSpellAssigner
    )

    @abstractmethod
    def _update_blueprint(self, blueprint: _BPT) -> _BPT: ...

    def apply[
        SubclassT: WizardSubclass,
        _StCK_: AnyStatChoices,
        _SkCK_: AnyStatChoices,
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
        blueprint: WizardLevel18Blueprint[
            _StCK_,
            _SkCK_,
            WizardSubclassLevel[LevelIn, SubclassT],
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
    ) -> WizardLevel20Blueprint[
        _StCK_,
        _SkCK_,
        WizardSubclassLevel[LevelOut, SubclassT],
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
        PositiveInt,
    ]:
        r1 = self._update_blueprint(blueprint)
        r2 = self.health_increase.apply(r1)
        wiz_r2 = WizardBlueprint[
            _StCK_,
            _SkCK_,
            WizardSubclassLevel[LevelOut, SubclassT],
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
        ].model_validate(
            dict(r2)
            | {
                "prepared_spells": blueprint.prepared_spells,
                "spell_slots": blueprint.spell_slots,
                "caster_level": blueprint.caster_level,
            }
        )
        r3 = self.spell_assigner.apply(wiz_r2)
        partial = WizardLevel20Blueprint[
            _StCK_,
            _SkCK_,
            WizardSubclassLevel[LevelOut, SubclassT],
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
            PositiveInt,
        ].model_validate(
            dict(r3)
            | {
                "spell_mastery_spells": blueprint.spell_mastery_spells,
                "signature_spells": (),
                "n_signature_spell_choices": 2,
            }
        )
        return partial.increase_full_caster()


class WizardSubclassFeatureLevelBase[
    LevelIn: AnyNonZeroWizardLevel,
    LevelOut: AnyNonZeroWizardLevel,
](BuildingBlock, ABC):
    """Base for wizard levels 6, 10, 14 that grant subclass-specific features."""

    health_increase: AnyD6HealthIncrease = Field(
        default_factory=D6HealthIncreaseAverage
    )
    spell_assigner: AnyWizardSpellAssigner = Field(
        default_factory=WizardRandomSpellAssigner
    )

    @abstractmethod
    def _update_blueprint(self, blueprint: _BPT) -> _BPT: ...

    def apply[
        _StCK_: AnyStatChoices,
        _SkCK_: AnyStatChoices,
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
        blueprint: WizardBlueprint[
            _StCK_,
            _SkCK_,
            LevelIn,
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
    ) -> WizardBlueprint[
        _StCK_,
        _SkCK_,
        LevelOut,
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
        r1 = self._update_blueprint(blueprint)
        r2 = self.health_increase.apply(r1)
        wiz_r2 = WizardBlueprint[
            _StCK_,
            _SkCK_,
            LevelOut,
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
        ].model_validate(
            dict(r2)
            | {
                "prepared_spells": blueprint.prepared_spells,
                "spell_slots": blueprint.spell_slots,
                "caster_level": blueprint.caster_level,
            }
        )
        r3 = self.spell_assigner.apply(wiz_r2)
        return r3.increase_full_caster()
