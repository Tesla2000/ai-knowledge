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
    RaceAssigner,
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
from dnd.character.blueprint.state import BlueprintProtocol
from dnd.character.blueprint.state import HasClasses
from dnd.character.blueprint.state import HasEquipmentChoices
from dnd.character.blueprint.state import HasFeats
from dnd.character.blueprint.state import HasLanguages
from dnd.character.blueprint.state import HasLevel
from dnd.character.blueprint.state import HasNSkillChoices
from dnd.character.blueprint.state import HasNStatChoices
from dnd.character.blueprint.state import HasOtherEquipment
from dnd.character.blueprint.state import HasSkillProficiencies
from dnd.character.blueprint.state import HasSkillsToChooseFrom
from dnd.character.blueprint.state import HasSorcererLevel
from dnd.character.blueprint.state import HasStats
from dnd.character.blueprint.state import HasStatsCup
from dnd.character.blueprint.state import HasSubclasses
from dnd.character.blueprint.state import HasToolProficiencies
from dnd.character.blueprint.state import HasWeapons
from dnd.character.blueprint.state import HasWizardLevel
from pydantic import Field
from typing_protocol_intersection import ProtocolIntersection

AnyBuildingBlock = Annotated[
    Union[
        AIAllChoicesResolver,
        AIAllNonStatChoicesResolver,
        AIBaseBuilderAssigner,
        AIEquipmentChooser[HasEquipmentChoices],
        AIFeatChoiceResolver[
            ProtocolIntersection[ProtocolIntersection[HasFeats, HasStats], HasClasses]
        ],
        AILanguageChoiceResolver[HasLanguages],
        AIMagicalItemChooser,
        AIPartialBuilderAssigner,
        AISkillChoiceResolver[
            ProtocolIntersection[
                ProtocolIntersection[HasNSkillChoices, HasSkillsToChooseFrom],
                HasSkillProficiencies,
            ]
        ],
        AIStatChoiceResolver[ProtocolIntersection[HasStats, HasNStatChoices]],
        AISubclassAssigner[ProtocolIntersection[HasClasses, HasSubclasses]],
        AIToolProficiencyChoiceResolver[HasToolProficiencies],
        ArtificerSubclassAssigner[ProtocolIntersection[HasClasses, HasSubclasses]],
        BarbarianSubclassAssigner[ProtocolIntersection[HasClasses, HasSubclasses]],
        BardSubclassAssigner[ProtocolIntersection[HasClasses, HasSubclasses]],
        ClericSubclassAssigner[ProtocolIntersection[HasClasses, HasSubclasses]],
        DruidSubclassAssigner[ProtocolIntersection[HasClasses, HasSubclasses]],
        FighterSubclassAssigner[ProtocolIntersection[HasClasses, HasSubclasses]],
        MonkSubclassAssigner[ProtocolIntersection[HasClasses, HasSubclasses]],
        PaladinSubclassAssigner[ProtocolIntersection[HasClasses, HasSubclasses]],
        RangerSubclassAssigner[ProtocolIntersection[HasClasses, HasSubclasses]],
        RogueSubclassAssigner[ProtocolIntersection[HasClasses, HasSubclasses]],
        SorcererSubclassAssigner[ProtocolIntersection[HasClasses, HasSubclasses]],
        WarlockSubclassAssigner[ProtocolIntersection[HasClasses, HasSubclasses]],
        WizardSubclassAssigner[ProtocolIntersection[HasClasses, HasSubclasses]],
        AgeAssigner[BlueprintProtocol],
        AlignmentAssigner[BlueprintProtocol],
        AllChoicesResolver,
        BackgroundAssigner[BlueprintProtocol],
        EquipmentAdder[HasOtherEquipment],
        FeatAdder[HasFeats],
        FeatureAssigner,
        HealthIncreaseAverage,
        HealthIncreaseRandom,
        HealthIncreaseRandomMinTwo,
        HealthIncreaseRandomRerollOnes,
        InitialBuilder,
        WizardLLMSpellAssigner[HasWizardLevel],
        SorcererLLMSpellAssigner[HasSorcererLevel],
        LevelAssigner[BlueprintProtocol],
        WizardLevelIncrementer[HasLevel],
        SorcererLevelIncrementer[HasLevel],
        LevelUp,
        LevelUpMultiple,
        MaxFirstResolver[
            ProtocolIntersection[
                ProtocolIntersection[
                    ProtocolIntersection[HasFeats, HasStats], HasClasses
                ],
                HasStatsCup,
            ]
        ],
        MaxIfNotMaxedResolver[
            ProtocolIntersection[
                ProtocolIntersection[
                    ProtocolIntersection[HasFeats, HasStats], HasClasses
                ],
                HasStatsCup,
            ]
        ],
        NameAssigner[BlueprintProtocol],
        NullBlock[BlueprintProtocol],
        OptionalSubclassAssigner[ProtocolIntersection[HasClasses, HasSubclasses]],
        PriorityStatChoiceResolver[ProtocolIntersection[HasStats, HasNStatChoices]],
        AarakocraRaceAssigner[HasStats],
        AasimarRaceAssigner[HasStats],
        BugbearRaceAssigner[HasStats],
        CentaurRaceAssigner[HasStats],
        ChangelingRaceAssigner[HasStats],
        DragonbornRaceAssigner[HasStats],
        DwarfRaceAssigner[HasStats],
        ElfRaceAssigner[HasStats],
        FirbolgRaceAssigner[HasStats],
        GenasiAirRaceAssigner[HasStats],
        GenasiEarthRaceAssigner[HasStats],
        GenasiFireRaceAssigner[HasStats],
        GenasiWaterRaceAssigner[HasStats],
        GnomeRaceAssigner[HasStats],
        GoblinRaceAssigner[HasStats],
        GoliathRaceAssigner[HasStats],
        GrungRaceAssigner[HasStats],
        HalfElfRaceAssigner[HasStats],
        HalflingRaceAssigner[HasStats],
        HalfOrcRaceAssigner[HasStats],
        HobgoblinRaceAssigner[HasStats],
        HumanRaceAssigner[HasStats],
        KalashtarRaceAssigner[HasStats],
        KenkuRaceAssigner[HasStats],
        KoboldRaceAssigner[HasStats],
        LeoninRaceAssigner[HasStats],
        LizardfolkRaceAssigner[HasStats],
        MinotaurRaceAssigner[HasStats],
        OrcRaceAssigner[HasStats],
        SatyrRaceAssigner[HasStats],
        ShifterRaceAssigner[HasStats],
        TabaxiRaceAssigner[HasStats],
        TieflingRaceAssigner[HasStats],
        TortleRaceAssigner[HasStats],
        VerdanRaceAssigner[HasStats],
        WarforgedRaceAssigner[HasStats],
        YuanTiPurebloodRaceAssigner[HasStats],
        RandomEquipmentChooser[HasEquipmentChoices],
        RandomFeatChoiceResolver[
            ProtocolIntersection[ProtocolIntersection[HasFeats, HasStats], HasClasses]
        ],
        RandomInitialDataFiller,
        RandomLanguageChoiceResolver[HasLanguages],
        RandomMagicalItemChooser,
        RandomRaceAssigner[HasStats],
        RaceAssigner[HasStats],
        RandomSkillChoiceResolver[
            ProtocolIntersection[
                ProtocolIntersection[HasNSkillChoices, HasSkillsToChooseFrom],
                HasSkillProficiencies,
            ]
        ],
        WizardRandomSpellAssigner[HasWizardLevel],
        SorcererRandomSpellAssigner[HasSorcererLevel],
        RandomSubclassAssigner[ProtocolIntersection[HasClasses, HasSubclasses]],
        RandomToolProficiencyChoiceResolver[HasToolProficiencies],
        SexAssigner[BlueprintProtocol],
        StandardArray[BlueprintProtocol],
        WeaponAdder[HasWeapons],
    ],
    Field(discriminator="type"),
]
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
    "RaceAssigner",
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
]
