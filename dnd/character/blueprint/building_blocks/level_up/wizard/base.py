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
from dnd.character.blueprint.states._caster_info import CasterInfo
from dnd.character.blueprint.states.state import Blueprint
from dnd.character.blueprint.states.state import _BPT
from dnd.character.blueprint.states.wizard._info import WizardInfo
from dnd.character.blueprint.states.wizard._info import WizardLevel18Info
from dnd.character.blueprint.states.wizard._info import WizardLevel20Info
from dnd.character.race.race import Race
from dnd.character.spells.max_spell_levels import FULL_CASTER_SPELL_SLOTS
from dnd.character.stats import Stats
from dnd.choices.class_creation.character_class import WizardSubclass
from pydantic import PositiveInt


class WizardUpgradeLevelBase[LevelOut: AnyNonZeroWizardLevel](
    BuildingBlock, ABC
):
    """Base for WizardLevel1: upgrades Blueprint[Race, Stats, ...] -> Blueprint[..., WizardInfo, CasterInfo, ...]."""

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
            None,
            None,
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
        Race,
        Stats,
        PositiveInt,
        _StCK_,
        _SkCK_,
        WizardInfo[LevelOut],
        CasterInfo,
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
        wizard_info: WizardInfo[LevelOut] = WizardInfo[LevelOut].model_validate(
            {"prepared_spells": ()}
        )
        caster_info = CasterInfo(spell_slots=FULL_CASTER_SPELL_SLOTS[0])
        interim = Blueprint[
            Race,
            Stats,
            PositiveInt,
            _StCK_,
            _SkCK_,
            WizardInfo[LevelOut],
            CasterInfo,
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
        ].model_validate(dict(r2) | {"wizard": wizard_info, "caster": caster_info})
        after_spells = self.spell_assigner.apply(interim)
        new_caster = after_spells.caster.increase_full_caster()
        return after_spells.model_copy(update={"caster": new_caster})


class WizardPreSubclassLevelBase[
    LevelIn: AnyNonZeroWizardLevel,
    LevelOut: AnyNonZeroWizardLevel,
](BuildingBlock, ABC):
    """Base for WizardLevel2*: Blueprint[..., WizardInfo[LevelIn], ...] -> Blueprint[..., WizardInfo[LevelOut], ...]."""

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
        blueprint: Blueprint[
            Race,
            Stats,
            PositiveInt,
            _StCK_,
            _SkCK_,
            WizardInfo[LevelIn],
            CasterInfo,
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
        Race,
        Stats,
        PositiveInt,
        _StCK_,
        _SkCK_,
        WizardInfo[LevelOut],
        CasterInfo,
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
        new_wizard: WizardInfo[LevelOut] = WizardInfo[LevelOut].model_validate(
            {"prepared_spells": blueprint.wizard.prepared_spells}
        )
        interim = Blueprint[
            Race,
            Stats,
            PositiveInt,
            _StCK_,
            _SkCK_,
            WizardInfo[LevelOut],
            CasterInfo,
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
                "wizard": new_wizard,
                "caster": blueprint.caster,
            }
        )
        after_spells = self.spell_assigner.apply(interim)
        new_caster = after_spells.caster.increase_full_caster()
        return after_spells.model_copy(update={"caster": new_caster})


class WizardSharedLevelBase[
    LevelIn: SecondSubclassPostLevel,
    LevelOut: SecondSubclassPostLevel,
](BuildingBlock, ABC):
    """Base for post-subclass wizard levels (3-20) shared across all subclasses."""

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
        blueprint: Blueprint[
            Race,
            Stats,
            PositiveInt,
            _StCK_,
            _SkCK_,
            WizardInfo[WizardSubclassLevel[LevelIn, SubclassT]],
            CasterInfo,
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
        Race,
        Stats,
        PositiveInt,
        _StCK_,
        _SkCK_,
        WizardInfo[WizardSubclassLevel[LevelOut, SubclassT]],
        CasterInfo,
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
        new_wizard: WizardInfo[WizardSubclassLevel[LevelOut, SubclassT]] = WizardInfo[
            WizardSubclassLevel[LevelOut, SubclassT]
        ].model_validate({"prepared_spells": blueprint.wizard.prepared_spells})
        interim = Blueprint[
            Race,
            Stats,
            PositiveInt,
            _StCK_,
            _SkCK_,
            WizardInfo[WizardSubclassLevel[LevelOut, SubclassT]],
            CasterInfo,
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
                "wizard": new_wizard,
                "caster": blueprint.caster,
            }
        )
        after_spells = self.spell_assigner.apply(interim)
        new_caster = after_spells.caster.increase_full_caster()
        return after_spells.model_copy(update={"caster": new_caster})


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
        blueprint: Blueprint[
            Race,
            Stats,
            PositiveInt,
            _StCK_,
            _SkCK_,
            WizardInfo[WizardSubclassLevel[LevelIn, SubclassT]],
            CasterInfo,
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
        Race,
        Stats,
        PositiveInt,
        _StCK_,
        _SkCK_,
        WizardInfo[WizardSubclassLevel[LevelOut, SubclassT]],
        CasterInfo,
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
    """Base for WizardLevel18: Blueprint[..., WizardInfo, ...] -> Blueprint[..., WizardLevel18Info, ...]."""

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
        blueprint: Blueprint[
            Race,
            Stats,
            PositiveInt,
            _StCK_,
            _SkCK_,
            WizardInfo[WizardSubclassLevel[LevelIn, SubclassT]],
            CasterInfo,
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
        Race,
        Stats,
        PositiveInt,
        _StCK_,
        _SkCK_,
        WizardLevel18Info[WizardSubclassLevel[LevelOut, SubclassT]],
        CasterInfo,
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
        interim_wizard: WizardInfo[WizardSubclassLevel[LevelOut, SubclassT]] = WizardInfo[
            WizardSubclassLevel[LevelOut, SubclassT]
        ].model_validate({"prepared_spells": blueprint.wizard.prepared_spells})
        interim = Blueprint[
            Race,
            Stats,
            PositiveInt,
            _StCK_,
            _SkCK_,
            WizardInfo[WizardSubclassLevel[LevelOut, SubclassT]],
            CasterInfo,
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
                "wizard": interim_wizard,
                "caster": blueprint.caster,
            }
        )
        after_spells = self.spell_assigner.apply(interim)
        new_wizard18: WizardLevel18Info[WizardSubclassLevel[LevelOut, SubclassT]] = WizardLevel18Info[
            WizardSubclassLevel[LevelOut, SubclassT]
        ].model_validate(
            dict(after_spells.wizard) | {"spell_mastery_spells": ()}
        )
        new_caster = after_spells.caster.increase_full_caster()
        return Blueprint[
            Race,
            Stats,
            PositiveInt,
            _StCK_,
            _SkCK_,
            WizardLevel18Info[WizardSubclassLevel[LevelOut, SubclassT]],
            CasterInfo,
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
            dict(after_spells) | {"wizard": new_wizard18, "caster": new_caster}
        )


class WizardPostLevel18SharedLevelBase[
    LevelIn: SecondSubclassPostLevel,
    LevelOut: SecondSubclassPostLevel,
](BuildingBlock, ABC):
    """Base for WizardLevel19: Blueprint[..., WizardLevel18Info, ...] -> Blueprint[..., WizardLevel18Info, ...]."""

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
        blueprint: Blueprint[
            Race,
            Stats,
            PositiveInt,
            _StCK_,
            _SkCK_,
            WizardLevel18Info[WizardSubclassLevel[LevelIn, SubclassT]],
            CasterInfo,
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
        Race,
        Stats,
        PositiveInt,
        _StCK_,
        _SkCK_,
        WizardLevel18Info[WizardSubclassLevel[LevelOut, SubclassT]],
        CasterInfo,
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
        interim_wizard: WizardInfo[WizardSubclassLevel[LevelOut, SubclassT]] = WizardInfo[
            WizardSubclassLevel[LevelOut, SubclassT]
        ].model_validate({"prepared_spells": blueprint.wizard.prepared_spells})
        interim = Blueprint[
            Race,
            Stats,
            PositiveInt,
            _StCK_,
            _SkCK_,
            WizardInfo[WizardSubclassLevel[LevelOut, SubclassT]],
            CasterInfo,
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
                "wizard": interim_wizard,
                "caster": blueprint.caster,
            }
        )
        after_spells = self.spell_assigner.apply(interim)
        new_wizard18: WizardLevel18Info[WizardSubclassLevel[LevelOut, SubclassT]] = WizardLevel18Info[
            WizardSubclassLevel[LevelOut, SubclassT]
        ].model_validate(
            dict(after_spells.wizard)
            | {"spell_mastery_spells": blueprint.wizard.spell_mastery_spells}
        )
        new_caster = after_spells.caster.increase_full_caster()
        return Blueprint[
            Race,
            Stats,
            PositiveInt,
            _StCK_,
            _SkCK_,
            WizardLevel18Info[WizardSubclassLevel[LevelOut, SubclassT]],
            CasterInfo,
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
            dict(after_spells) | {"wizard": new_wizard18, "caster": new_caster}
        )


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
        blueprint: Blueprint[
            Race,
            Stats,
            PositiveInt,
            _StCK_,
            _SkCK_,
            WizardLevel18Info[WizardSubclassLevel[LevelIn, SubclassT]],
            CasterInfo,
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
        Race,
        Stats,
        PositiveInt,
        _StCK_,
        _SkCK_,
        WizardLevel18Info[WizardSubclassLevel[LevelOut, SubclassT]],
        CasterInfo,
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
    """Base for WizardLevel20: Blueprint[..., WizardLevel18Info, ...] -> Blueprint[..., WizardLevel20Info, ...]."""

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
        blueprint: Blueprint[
            Race,
            Stats,
            PositiveInt,
            _StCK_,
            _SkCK_,
            WizardLevel18Info[WizardSubclassLevel[LevelIn, SubclassT]],
            CasterInfo,
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
        Race,
        Stats,
        PositiveInt,
        _StCK_,
        _SkCK_,
        WizardLevel20Info[WizardSubclassLevel[LevelOut, SubclassT]],
        CasterInfo,
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
        interim_wizard: WizardInfo[WizardSubclassLevel[LevelOut, SubclassT]] = WizardInfo[
            WizardSubclassLevel[LevelOut, SubclassT]
        ].model_validate({"prepared_spells": blueprint.wizard.prepared_spells})
        interim = Blueprint[
            Race,
            Stats,
            PositiveInt,
            _StCK_,
            _SkCK_,
            WizardInfo[WizardSubclassLevel[LevelOut, SubclassT]],
            CasterInfo,
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
                "wizard": interim_wizard,
                "caster": blueprint.caster,
            }
        )
        after_spells = self.spell_assigner.apply(interim)
        new_wizard20: WizardLevel20Info[WizardSubclassLevel[LevelOut, SubclassT]] = WizardLevel20Info[
            WizardSubclassLevel[LevelOut, SubclassT]
        ].model_validate(
            dict(after_spells.wizard)
            | {
                "spell_mastery_spells": blueprint.wizard.spell_mastery_spells,
                "signature_spells": (),
                "n_signature_spell_choices": 2,
            }
        )
        new_caster = after_spells.caster.increase_full_caster()
        return Blueprint[
            Race,
            Stats,
            PositiveInt,
            _StCK_,
            _SkCK_,
            WizardLevel20Info[WizardSubclassLevel[LevelOut, SubclassT]],
            CasterInfo,
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
            dict(after_spells) | {"wizard": new_wizard20, "caster": new_caster}
        )


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
        blueprint: Blueprint[
            Race,
            Stats,
            PositiveInt,
            _StCK_,
            _SkCK_,
            WizardInfo[LevelIn],
            CasterInfo,
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
        Race,
        Stats,
        PositiveInt,
        _StCK_,
        _SkCK_,
        WizardInfo[LevelOut],
        CasterInfo,
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
        new_wizard: WizardInfo[LevelOut] = WizardInfo[LevelOut].model_validate(
            {"prepared_spells": blueprint.wizard.prepared_spells}
        )
        interim = Blueprint[
            Race,
            Stats,
            PositiveInt,
            _StCK_,
            _SkCK_,
            WizardInfo[LevelOut],
            CasterInfo,
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
                "wizard": new_wizard,
                "caster": blueprint.caster,
            }
        )
        after_spells = self.spell_assigner.apply(interim)
        new_caster = after_spells.caster.increase_full_caster()
        return after_spells.model_copy(update={"caster": new_caster})
