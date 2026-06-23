from __future__ import annotations

from typing import Annotated
from typing import Union

from dnd.character.blueprint.building_blocks.age_assigner import (
    AgeAssigner,
)
from dnd.character.blueprint.building_blocks.alignment_assigner import (
    AlignmentAssigner,
)
from dnd.character.blueprint.building_blocks.all_choices_resolver import (
    AIAllChoicesResolver,
)
from dnd.character.blueprint.building_blocks.all_choices_resolver.ai import (
    AIAllNonStatChoicesResolver,
)
from dnd.character.blueprint.building_blocks.all_choices_resolver import (
    AllChoicesResolver,
)
from dnd.character.blueprint.building_blocks.background_assigner import (
    BackgroundAssigner,
)
from dnd.character.blueprint.building_blocks.building_block import (
    CombinedBlock,
)
from dnd.character.blueprint.building_blocks.character_base_template import (
    CharacterBaseTemplate,
)
from dnd.character.blueprint.building_blocks.equipment_adder import (
    EquipmentAdder,
)
from dnd.character.blueprint.building_blocks.equipment_chooser import (
    AIEquipmentChooser,
)
from dnd.character.blueprint.building_blocks.equipment_chooser import (
    RandomEquipmentChooser,
)
from dnd.character.blueprint.building_blocks.feat_adder import (
    FeatAdder,
)
from dnd.character.blueprint.building_blocks.feat_choice_resolver import (
    AIFeatChoiceResolver,
)
from dnd.character.blueprint.building_blocks.feat_choice_resolver import (
    MaxFirstResolver,
)
from dnd.character.blueprint.building_blocks.feat_choice_resolver import (
    MaxIfNotMaxedResolver,
)
from dnd.character.blueprint.building_blocks.feat_choice_resolver import (
    RandomFeatChoiceResolver,
)
from dnd.character.blueprint.building_blocks.feature_assigner import (
    FeatureAssigner,
)
from dnd.character.blueprint.building_blocks.get_discriminator import (
    get_discriminator,
)
from dnd.character.blueprint.building_blocks.initial_builder import (
    InitialBuilder,
)
from dnd.character.blueprint.building_blocks.initial_data_filler import (
    AIBaseBuilderAssigner,
)
from dnd.character.blueprint.building_blocks.initial_data_filler import (
    AIPartialBuilderAssigner,
)
from dnd.character.blueprint.building_blocks.initial_data_filler import (
    RandomInitialDataFiller,
)
from dnd.character.blueprint.building_blocks.language_choice_resolver import (
    AILanguageChoiceResolver,
)
from dnd.character.blueprint.building_blocks.language_choice_resolver import (
    RandomLanguageChoiceResolver,
)
from dnd.character.blueprint.building_blocks.level_assigner import (
    LevelAssigner,
)
from dnd.character.blueprint.building_blocks.level_up.health_increase import (
    HealthIncreaseAverage,
)
from dnd.character.blueprint.building_blocks.level_up.health_increase import (
    HealthIncreaseRandom,
)
from dnd.character.blueprint.building_blocks.level_up.health_increase import (
    HealthIncreaseRandomMinTwo,
)
from dnd.character.blueprint.building_blocks.level_up.health_increase import (
    HealthIncreaseRandomRerollOnes,
)
from dnd.character.blueprint.building_blocks.level_up.level_incrementer import (
    SorcererLevelIncrementer,
    WizardLevelIncrementer,
)
from dnd.character.blueprint.building_blocks.level_up.level_up import (
    LevelUp,
)
from dnd.character.blueprint.building_blocks.level_up.level_up_multiple import (
    LevelUpMultiple,
)
from dnd.character.blueprint.building_blocks.level_up.spell_assignment import (
    SorcererLLMSpellAssigner,
)
from dnd.character.blueprint.building_blocks.level_up.spell_assignment import (
    SorcererRandomSpellAssigner,
)
from dnd.character.blueprint.building_blocks.level_up.spell_assignment import (
    WizardLLMSpellAssigner,
)
from dnd.character.blueprint.building_blocks.level_up.spell_assignment import (
    WizardRandomSpellAssigner,
)
from dnd.character.blueprint.building_blocks.magical_item_chooser import (
    AIMagicalItemChooser,
)
from dnd.character.blueprint.building_blocks.magical_item_chooser import (
    RandomMagicalItemChooser,
)
from dnd.character.blueprint.building_blocks.name_assigner import (
    NameAssigner,
)
from dnd.character.blueprint.building_blocks.null_block import (
    NullBlock,
)
from dnd.character.blueprint.building_blocks.race_assigner import (
    AarakocraRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner import (
    AasimarRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner import (
    BugbearRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner import (
    CentaurRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner import (
    ChangelingRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner import (
    DragonbornRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner import (
    DwarfRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner import (
    ElfRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner import (
    FirbolgRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner import (
    GenasiAirRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner import (
    GenasiEarthRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner import (
    GenasiFireRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner import (
    GenasiWaterRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner import (
    GnomeRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner import (
    GoblinRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner import (
    GoliathRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner import (
    GrungRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner import (
    HalfElfRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner import (
    HalflingRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner import (
    HalfOrcRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner import (
    HobgoblinRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner import (
    HumanRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner import (
    KalashtarRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner import (
    KenkuRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner import (
    KoboldRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner import (
    LeoninRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner import (
    LizardfolkRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner import (
    MinotaurRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner import (
    OrcRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner import (
    RandomRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner import (
    SatyrRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner import (
    ShifterRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner import (
    TabaxiRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner import (
    TieflingRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner import (
    TortleRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner import (
    VerdanRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner import (
    WarforgedRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner import (
    YuanTiPurebloodRaceAssigner,
)
from dnd.character.blueprint.building_blocks.sex_assigner import (
    SexAssigner,
)
from dnd.character.blueprint.building_blocks.skill_choice_resolver import (
    AISkillChoiceResolver,
)
from dnd.character.blueprint.building_blocks.skill_choice_resolver import (
    RandomSkillChoiceResolver,
)
from dnd.character.blueprint.building_blocks.stat_choice_resolver import (
    AIStatChoiceResolver,
)
from dnd.character.blueprint.building_blocks.stat_choice_resolver import (
    PriorityStatChoiceResolver,
)
from dnd.character.blueprint.building_blocks.stats_builder.standard_array import (
    StandardArray,
)
from dnd.character.blueprint.building_blocks.subclass_assigner import (
    AISubclassAssigner,
)
from dnd.character.blueprint.building_blocks.subclass_assigner import (
    ArtificerSubclassAssigner,
)
from dnd.character.blueprint.building_blocks.subclass_assigner import (
    BarbarianSubclassAssigner,
)
from dnd.character.blueprint.building_blocks.subclass_assigner import (
    BardSubclassAssigner,
)
from dnd.character.blueprint.building_blocks.subclass_assigner import (
    ClericSubclassAssigner,
)
from dnd.character.blueprint.building_blocks.subclass_assigner import (
    DruidSubclassAssigner,
)
from dnd.character.blueprint.building_blocks.subclass_assigner import (
    FighterSubclassAssigner,
)
from dnd.character.blueprint.building_blocks.subclass_assigner import (
    MonkSubclassAssigner,
)
from dnd.character.blueprint.building_blocks.subclass_assigner import (
    OptionalSubclassAssigner,
)
from dnd.character.blueprint.building_blocks.subclass_assigner import (
    PaladinSubclassAssigner,
)
from dnd.character.blueprint.building_blocks.subclass_assigner import (
    RangerSubclassAssigner,
)
from dnd.character.blueprint.building_blocks.subclass_assigner import (
    RandomSubclassAssigner,
)
from dnd.character.blueprint.building_blocks.subclass_assigner import (
    RogueSubclassAssigner,
)
from dnd.character.blueprint.building_blocks.subclass_assigner import (
    SorcererSubclassAssigner,
)
from dnd.character.blueprint.building_blocks.subclass_assigner import (
    WarlockSubclassAssigner,
)
from dnd.character.blueprint.building_blocks.subclass_assigner import (
    WizardSubclassAssigner,
)
from dnd.character.blueprint.building_blocks.tool_proficiency_choice_resolver import (
    AIToolProficiencyChoiceResolver,
)
from dnd.character.blueprint.building_blocks.tool_proficiency_choice_resolver import (
    RandomToolProficiencyChoiceResolver,
)
from dnd.character.blueprint.building_blocks.weapon_adder import (
    WeaponAdder,
)
from pydantic import Tag

AnyBuildingBlock = Annotated[
    Union[
        Annotated[AIAllChoicesResolver, Tag("AIAllChoicesResolver")],
        Annotated[AIAllNonStatChoicesResolver, Tag("AIAllNonStatChoicesResolver")],
        Annotated[AIBaseBuilderAssigner, Tag("AIBaseBuilderAssigner")],
        Annotated[AIEquipmentChooser, Tag("AIEquipmentChooser")],
        Annotated[AIFeatChoiceResolver, Tag("AIFeatChoiceResolver")],
        Annotated[AILanguageChoiceResolver, Tag("AILanguageChoiceResolver")],
        Annotated[AIMagicalItemChooser, Tag("AIMagicalItemChooser")],
        Annotated[AIPartialBuilderAssigner, Tag("AIPartialBuilderAssigner")],
        Annotated[AISkillChoiceResolver, Tag("AISkillChoiceResolver")],
        Annotated[AIStatChoiceResolver, Tag("AIStatChoiceResolver")],
        Annotated[AISubclassAssigner, Tag("AISubclassAssigner")],
        Annotated[
            AIToolProficiencyChoiceResolver, Tag("AIToolProficiencyChoiceResolver")
        ],
        Annotated[ArtificerSubclassAssigner, Tag("ArtificerSubclassAssigner")],
        Annotated[BarbarianSubclassAssigner, Tag("BarbarianSubclassAssigner")],
        Annotated[BardSubclassAssigner, Tag("BardSubclassAssigner")],
        Annotated[ClericSubclassAssigner, Tag("ClericSubclassAssigner")],
        Annotated[DruidSubclassAssigner, Tag("DruidSubclassAssigner")],
        Annotated[FighterSubclassAssigner, Tag("FighterSubclassAssigner")],
        Annotated[MonkSubclassAssigner, Tag("MonkSubclassAssigner")],
        Annotated[PaladinSubclassAssigner, Tag("PaladinSubclassAssigner")],
        Annotated[RangerSubclassAssigner, Tag("RangerSubclassAssigner")],
        Annotated[RogueSubclassAssigner, Tag("RogueSubclassAssigner")],
        Annotated[SorcererSubclassAssigner, Tag("SorcererSubclassAssigner")],
        Annotated[WarlockSubclassAssigner, Tag("WarlockSubclassAssigner")],
        Annotated[WizardSubclassAssigner, Tag("WizardSubclassAssigner")],
        Annotated[AgeAssigner, Tag("AgeAssigner")],
        Annotated[AlignmentAssigner, Tag("AlignmentAssigner")],
        Annotated[AllChoicesResolver, Tag("AllChoicesResolver")],
        Annotated[BackgroundAssigner, Tag("BackgroundAssigner")],
        Annotated[CombinedBlock, Tag("CombinedBlock")],
        Annotated[EquipmentAdder, Tag("EquipmentAdder")],
        Annotated[FeatAdder, Tag("FeatAdder")],
        Annotated[FeatureAssigner, Tag("FeatureAssigner")],
        Annotated[HealthIncreaseAverage, Tag("HealthIncreaseAverage")],
        Annotated[HealthIncreaseRandom, Tag("HealthIncreaseRandom")],
        Annotated[HealthIncreaseRandomMinTwo, Tag("HealthIncreaseRandomMinTwo")],
        Annotated[
            HealthIncreaseRandomRerollOnes, Tag("HealthIncreaseRandomRerollOnes")
        ],
        Annotated[InitialBuilder, Tag("InitialBuilder")],
        Annotated[WizardLLMSpellAssigner, Tag("WizardLLMSpellAssigner")],
        Annotated[SorcererLLMSpellAssigner, Tag("SorcererLLMSpellAssigner")],
        Annotated[LevelAssigner, Tag("LevelAssigner")],
        Annotated[WizardLevelIncrementer, Tag("WizardLevelIncrementer")],
        Annotated[SorcererLevelIncrementer, Tag("SorcererLevelIncrementer")],
        Annotated[LevelUp, Tag("LevelUp")],
        Annotated[LevelUpMultiple, Tag("LevelUpMultiple")],
        Annotated[MaxFirstResolver, Tag("MaxFirstResolver")],
        Annotated[MaxIfNotMaxedResolver, Tag("MaxIfNotMaxedResolver")],
        Annotated[NameAssigner, Tag("NameAssigner")],
        Annotated[NullBlock, Tag("NullBlock")],
        Annotated[OptionalSubclassAssigner, Tag("OptionalSubclassAssigner")],
        Annotated[PriorityStatChoiceResolver, Tag("PriorityStatChoiceResolver")],
        Annotated[AarakocraRaceAssigner, Tag("AarakocraRaceAssigner")],
        Annotated[AasimarRaceAssigner, Tag("AasimarRaceAssigner")],
        Annotated[BugbearRaceAssigner, Tag("BugbearRaceAssigner")],
        Annotated[CentaurRaceAssigner, Tag("CentaurRaceAssigner")],
        Annotated[ChangelingRaceAssigner, Tag("ChangelingRaceAssigner")],
        Annotated[DragonbornRaceAssigner, Tag("DragonbornRaceAssigner")],
        Annotated[DwarfRaceAssigner, Tag("DwarfRaceAssigner")],
        Annotated[ElfRaceAssigner, Tag("ElfRaceAssigner")],
        Annotated[FirbolgRaceAssigner, Tag("FirbolgRaceAssigner")],
        Annotated[GenasiAirRaceAssigner, Tag("GenasiAirRaceAssigner")],
        Annotated[GenasiEarthRaceAssigner, Tag("GenasiEarthRaceAssigner")],
        Annotated[GenasiFireRaceAssigner, Tag("GenasiFireRaceAssigner")],
        Annotated[GenasiWaterRaceAssigner, Tag("GenasiWaterRaceAssigner")],
        Annotated[GnomeRaceAssigner, Tag("GnomeRaceAssigner")],
        Annotated[GoblinRaceAssigner, Tag("GoblinRaceAssigner")],
        Annotated[GoliathRaceAssigner, Tag("GoliathRaceAssigner")],
        Annotated[GrungRaceAssigner, Tag("GrungRaceAssigner")],
        Annotated[HalfElfRaceAssigner, Tag("HalfElfRaceAssigner")],
        Annotated[HalflingRaceAssigner, Tag("HalflingRaceAssigner")],
        Annotated[HalfOrcRaceAssigner, Tag("HalfOrcRaceAssigner")],
        Annotated[HobgoblinRaceAssigner, Tag("HobgoblinRaceAssigner")],
        Annotated[HumanRaceAssigner, Tag("HumanRaceAssigner")],
        Annotated[KalashtarRaceAssigner, Tag("KalashtarRaceAssigner")],
        Annotated[KenkuRaceAssigner, Tag("KenkuRaceAssigner")],
        Annotated[KoboldRaceAssigner, Tag("KoboldRaceAssigner")],
        Annotated[LeoninRaceAssigner, Tag("LeoninRaceAssigner")],
        Annotated[LizardfolkRaceAssigner, Tag("LizardfolkRaceAssigner")],
        Annotated[MinotaurRaceAssigner, Tag("MinotaurRaceAssigner")],
        Annotated[OrcRaceAssigner, Tag("OrcRaceAssigner")],
        Annotated[SatyrRaceAssigner, Tag("SatyrRaceAssigner")],
        Annotated[ShifterRaceAssigner, Tag("ShifterRaceAssigner")],
        Annotated[TabaxiRaceAssigner, Tag("TabaxiRaceAssigner")],
        Annotated[TieflingRaceAssigner, Tag("TieflingRaceAssigner")],
        Annotated[TortleRaceAssigner, Tag("TortleRaceAssigner")],
        Annotated[VerdanRaceAssigner, Tag("VerdanRaceAssigner")],
        Annotated[WarforgedRaceAssigner, Tag("WarforgedRaceAssigner")],
        Annotated[YuanTiPurebloodRaceAssigner, Tag("YuanTiPurebloodRaceAssigner")],
        Annotated[RandomEquipmentChooser, Tag("RandomEquipmentChooser")],
        Annotated[RandomFeatChoiceResolver, Tag("RandomFeatChoiceResolver")],
        Annotated[RandomInitialDataFiller, Tag("RandomInitialDataFiller")],
        Annotated[RandomLanguageChoiceResolver, Tag("RandomLanguageChoiceResolver")],
        Annotated[RandomMagicalItemChooser, Tag("RandomMagicalItemChooser")],
        Annotated[RandomRaceAssigner, Tag("RandomRaceAssigner")],
        Annotated[RandomSkillChoiceResolver, Tag("RandomSkillChoiceResolver")],
        Annotated[WizardRandomSpellAssigner, Tag("WizardRandomSpellAssigner")],
        Annotated[SorcererRandomSpellAssigner, Tag("SorcererRandomSpellAssigner")],
        Annotated[RandomSubclassAssigner, Tag("RandomSubclassAssigner")],
        Annotated[
            RandomToolProficiencyChoiceResolver,
            Tag("RandomToolProficiencyChoiceResolver"),
        ],
        Annotated[SexAssigner, Tag("SexAssigner")],
        Annotated[StandardArray, Tag("StandardArray")],
        Annotated[WeaponAdder, Tag("WeaponAdder")],
    ],
    get_discriminator(),
]
AnyBlocks = tuple[AnyBuildingBlock, ...]
CombinedBlock.model_rebuild(force=True, _types_namespace={"AnyBlocks": AnyBlocks})
Blocks = AnyBlocks
__all__ = [
    "AgeAssigner",
    "AIBaseBuilderAssigner",
    "AIAllChoicesResolver",
    "AIEquipmentChooser",
    "AIFeatChoiceResolver",
    "AILanguageChoiceResolver",
    "AIMagicalItemChooser",
    "AIPartialBuilderAssigner",
    "AISkillChoiceResolver",
    "AIStatChoiceResolver",
    "AIToolProficiencyChoiceResolver",
    "AllChoicesResolver",
    "AlignmentAssigner",
    "BackgroundAssigner",
    "CharacterBaseTemplate",
    "EquipmentAdder",
    "FeatAdder",
    "FeatureAssigner",
    "HealthIncreaseAverage",
    "HealthIncreaseRandom",
    "HealthIncreaseRandomMinTwo",
    "HealthIncreaseRandomRerollOnes",
    "LevelAssigner",
    "WizardLevelIncrementer",
    "SorcererLevelIncrementer",
    "LevelUp",
    "LevelUpMultiple",
    "WizardLLMSpellAssigner",
    "SorcererLLMSpellAssigner",
    "MaxFirstResolver",
    "MaxIfNotMaxedResolver",
    "NameAssigner",
    "InitialBuilder",
    "OptionalSubclassAssigner",
    "PriorityStatChoiceResolver",
    "AarakocraRaceAssigner",
    "AasimarRaceAssigner",
    "BugbearRaceAssigner",
    "CentaurRaceAssigner",
    "ChangelingRaceAssigner",
    "DragonbornRaceAssigner",
    "DwarfRaceAssigner",
    "ElfRaceAssigner",
    "FirbolgRaceAssigner",
    "GenasiAirRaceAssigner",
    "GenasiEarthRaceAssigner",
    "GenasiFireRaceAssigner",
    "GenasiWaterRaceAssigner",
    "GnomeRaceAssigner",
    "GoblinRaceAssigner",
    "GoliathRaceAssigner",
    "GrungRaceAssigner",
    "HalfElfRaceAssigner",
    "HalflingRaceAssigner",
    "HalfOrcRaceAssigner",
    "HobgoblinRaceAssigner",
    "HumanRaceAssigner",
    "KalashtarRaceAssigner",
    "KenkuRaceAssigner",
    "KoboldRaceAssigner",
    "LeoninRaceAssigner",
    "LizardfolkRaceAssigner",
    "MinotaurRaceAssigner",
    "OrcRaceAssigner",
    "SatyrRaceAssigner",
    "ShifterRaceAssigner",
    "TabaxiRaceAssigner",
    "TieflingRaceAssigner",
    "TortleRaceAssigner",
    "VerdanRaceAssigner",
    "WarforgedRaceAssigner",
    "YuanTiPurebloodRaceAssigner",
    "RandomEquipmentChooser",
    "RandomFeatChoiceResolver",
    "RandomInitialDataFiller",
    "RandomLanguageChoiceResolver",
    "RandomMagicalItemChooser",
    "RandomRaceAssigner",
    "RandomSkillChoiceResolver",
    "WizardRandomSpellAssigner",
    "SorcererRandomSpellAssigner",
    "RandomToolProficiencyChoiceResolver",
    "AISubclassAssigner",
    "ArtificerSubclassAssigner",
    "BarbarianSubclassAssigner",
    "BardSubclassAssigner",
    "ClericSubclassAssigner",
    "DruidSubclassAssigner",
    "FighterSubclassAssigner",
    "MonkSubclassAssigner",
    "PaladinSubclassAssigner",
    "RangerSubclassAssigner",
    "RandomSubclassAssigner",
    "RogueSubclassAssigner",
    "SorcererSubclassAssigner",
    "WarlockSubclassAssigner",
    "WizardSubclassAssigner",
    "SexAssigner",
    "StandardArray",
    "WeaponAdder",
    "AnyBuildingBlock",
    "Blocks",
    "CombinedBlock",
]
