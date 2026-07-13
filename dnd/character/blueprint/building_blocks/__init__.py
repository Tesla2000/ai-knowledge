from typing import Annotated
from typing import Union

from dnd.character.blueprint.building_blocks.all_choices_resolver import (
    AIAllChoicesResolver,
)
from dnd.character.blueprint.building_blocks.all_choices_resolver.ai import (
    AIAllNonStatChoicesResolver,
)
from dnd.character.blueprint.building_blocks.all_choices_resolver import (
    AllChoicesResolver,
)
from dnd.character.blueprint.building_blocks.character_base_template import (
    CharacterBaseTemplate,
)
from dnd.character.blueprint.building_blocks.character_data_assigner import (
    CharacterDataAssigner,
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
from dnd.character.blueprint.building_blocks.character_converter import (
    CharacterConverter,
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
from dnd.character.blueprint.building_blocks.level_up.wizard.level_1 import (
    WizardLevel1,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.level_3 import (
    WizardLevel3,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.level_4 import (
    WizardLevel4,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.level_5 import (
    WizardLevel5,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.level_7 import (
    WizardLevel7,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.level_8 import (
    WizardLevel8,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.level_9 import (
    WizardLevel9,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.level_11 import (
    WizardLevel11,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.level_12 import (
    WizardLevel12,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.level_13 import (
    WizardLevel13,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.level_15 import (
    WizardLevel15,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.level_16 import (
    WizardLevel16,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.level_17 import (
    WizardLevel17,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.level_18 import (
    WizardLevel18,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.level_19 import (
    WizardLevel19,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.level_20 import (
    WizardLevel20,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.abjuration.level_2 import (
    WizardLevel2Abjuration,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.abjuration.level_6 import (
    WizardLevel6Abjuration,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.abjuration.level_10 import (
    WizardLevel10Abjuration,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.abjuration.level_14 import (
    WizardLevel14Abjuration,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.bladesinging.level_2 import (
    WizardLevel2Bladesinging,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.bladesinging.level_6 import (
    WizardLevel6Bladesinging,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.bladesinging.level_10 import (
    WizardLevel10Bladesinging,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.bladesinging.level_14 import (
    WizardLevel14Bladesinging,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.chronurgy.level_2 import (
    WizardLevel2Chronurgy,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.chronurgy.level_6 import (
    WizardLevel6Chronurgy,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.chronurgy.level_10 import (
    WizardLevel10Chronurgy,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.chronurgy.level_14 import (
    WizardLevel14Chronurgy,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.conjuration.level_2 import (
    WizardLevel2Conjuration,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.conjuration.level_6 import (
    WizardLevel6Conjuration,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.conjuration.level_10 import (
    WizardLevel10Conjuration,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.conjuration.level_14 import (
    WizardLevel14Conjuration,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.divination.level_2 import (
    WizardLevel2Divination,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.divination.level_6 import (
    WizardLevel6Divination,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.divination.level_10 import (
    WizardLevel10Divination,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.divination.level_14 import (
    WizardLevel14Divination,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.enchantment.level_2 import (
    WizardLevel2Enchantment,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.enchantment.level_6 import (
    WizardLevel6Enchantment,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.enchantment.level_10 import (
    WizardLevel10Enchantment,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.enchantment.level_14 import (
    WizardLevel14Enchantment,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.evocation.level_2 import (
    WizardLevel2Evocation,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.evocation.level_6 import (
    WizardLevel6Evocation,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.evocation.level_10 import (
    WizardLevel10Evocation,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.evocation.level_14 import (
    WizardLevel14Evocation,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.graviturgy.level_2 import (
    WizardLevel2Graviturgy,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.graviturgy.level_6 import (
    WizardLevel6Graviturgy,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.graviturgy.level_10 import (
    WizardLevel10Graviturgy,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.graviturgy.level_14 import (
    WizardLevel14Graviturgy,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.illusion.level_2 import (
    WizardLevel2Illusion,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.illusion.level_6 import (
    WizardLevel6Illusion,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.illusion.level_10 import (
    WizardLevel10Illusion,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.illusion.level_14 import (
    WizardLevel14Illusion,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.necromancy.level_2 import (
    WizardLevel2Necromancy,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.necromancy.level_6 import (
    WizardLevel6Necromancy,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.necromancy.level_10 import (
    WizardLevel10Necromancy,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.necromancy.level_14 import (
    WizardLevel14Necromancy,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.scribes.level_2 import (
    WizardLevel2Scribes,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.scribes.level_6 import (
    WizardLevel6Scribes,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.scribes.level_10 import (
    WizardLevel10Scribes,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.scribes.level_14 import (
    WizardLevel14Scribes,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.transmutation.level_2 import (
    WizardLevel2Transmutation,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.transmutation.level_6 import (
    WizardLevel6Transmutation,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.transmutation.level_10 import (
    WizardLevel10Transmutation,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.transmutation.level_14 import (
    WizardLevel14Transmutation,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.war_magic.level_2 import (
    WizardLevel2WarMagic,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.war_magic.level_6 import (
    WizardLevel6WarMagic,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.war_magic.level_10 import (
    WizardLevel10WarMagic,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.war_magic.level_14 import (
    WizardLevel14WarMagic,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.level_2 import (
    SorcererLevel2,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.level_3 import (
    SorcererLevel3,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.level_4 import (
    SorcererLevel4,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.level_5 import (
    SorcererLevel5,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.level_7 import (
    SorcererLevel7,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.level_8 import (
    SorcererLevel8,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.level_9 import (
    SorcererLevel9,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.level_10 import (
    SorcererLevel10,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.level_11 import (
    SorcererLevel11,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.level_12 import (
    SorcererLevel12,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.level_13 import (
    SorcererLevel13,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.level_15 import (
    SorcererLevel15,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.level_16 import (
    SorcererLevel16,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.level_17 import (
    SorcererLevel17,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.level_19 import (
    SorcererLevel19,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.level_20 import (
    SorcererLevel20,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.aberrant_mind.level_1 import (
    SorcererLevel1AberrantMind,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.aberrant_mind.level_6 import (
    SorcererLevel6AberrantMind,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.aberrant_mind.level_14 import (
    SorcererLevel14AberrantMind,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.aberrant_mind.level_18 import (
    SorcererLevel18AberrantMind,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.clockwork_soul.level_1 import (
    SorcererLevel1ClockworkSoul,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.clockwork_soul.level_6 import (
    SorcererLevel6ClockworkSoul,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.clockwork_soul.level_14 import (
    SorcererLevel14ClockworkSoul,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.clockwork_soul.level_18 import (
    SorcererLevel18ClockworkSoul,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.draconic_bloodline.level_1 import (
    SorcererLevel1DraconicBloodline,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.draconic_bloodline.level_6 import (
    SorcererLevel6DraconicBloodline,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.draconic_bloodline.level_14 import (
    SorcererLevel14DraconicBloodline,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.draconic_bloodline.level_18 import (
    SorcererLevel18DraconicBloodline,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.divine_soul.level_1 import (
    SorcererLevel1DivineSoul,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.divine_soul.level_6 import (
    SorcererLevel6DivineSoul,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.divine_soul.level_14 import (
    SorcererLevel14DivineSoul,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.divine_soul.level_18 import (
    SorcererLevel18DivineSoul,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.lunar_sorcery.level_1 import (
    SorcererLevel1LunarSorcery,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.lunar_sorcery.level_6 import (
    SorcererLevel6LunarSorcery,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.lunar_sorcery.level_14 import (
    SorcererLevel14LunarSorcery,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.lunar_sorcery.level_18 import (
    SorcererLevel18LunarSorcery,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.shadow_magic.level_1 import (
    SorcererLevel1ShadowMagic,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.shadow_magic.level_6 import (
    SorcererLevel6ShadowMagic,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.shadow_magic.level_14 import (
    SorcererLevel14ShadowMagic,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.shadow_magic.level_18 import (
    SorcererLevel18ShadowMagic,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.storm_sorcery.level_1 import (
    SorcererLevel1StormSorcery,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.storm_sorcery.level_6 import (
    SorcererLevel6StormSorcery,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.storm_sorcery.level_14 import (
    SorcererLevel14StormSorcery,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.storm_sorcery.level_18 import (
    SorcererLevel18StormSorcery,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.wild_magic.level_1 import (
    SorcererLevel1WildMagic,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.wild_magic.level_6 import (
    SorcererLevel6WildMagic,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.wild_magic.level_14 import (
    SorcererLevel14WildMagic,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.wild_magic.level_18 import (
    SorcererLevel18WildMagic,
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
from dnd.character.blueprint.building_blocks.age_assigner import (
    AgeAssigner,
)
from dnd.character.blueprint.building_blocks.alignment_assigner import (
    AlignmentAssigner,
)
from dnd.character.blueprint.building_blocks.background_assigner import (
    BackgroundAssigner,
)
from dnd.character.blueprint.building_blocks.name_assigner import (
    NameAssigner,
)
from dnd.character.blueprint.building_blocks.sex_assigner import (
    SexAssigner,
)
from pydantic import Field

AnyBuildingBlock = Annotated[
    Union[
        AIAllChoicesResolver,
        AIAllNonStatChoicesResolver,
        AIBaseBuilderAssigner,
        AIEquipmentChooser,
        AIFeatChoiceResolver,
        AILanguageChoiceResolver,
        AIMagicalItemChooser,
        AIPartialBuilderAssigner,
        AISkillChoiceResolver,
        AIStatChoiceResolver,
        AISubclassAssigner,
        AIToolProficiencyChoiceResolver,
        ArtificerSubclassAssigner,
        BarbarianSubclassAssigner,
        BardSubclassAssigner,
        ClericSubclassAssigner,
        DruidSubclassAssigner,
        FighterSubclassAssigner,
        MonkSubclassAssigner,
        PaladinSubclassAssigner,
        RangerSubclassAssigner,
        RogueSubclassAssigner,
        SorcererSubclassAssigner,
        WarlockSubclassAssigner,
        WizardSubclassAssigner,
        AllChoicesResolver,
        CharacterDataAssigner,
        EquipmentAdder,
        FeatAdder,
        FeatureAssigner,
        HealthIncreaseAverage,
        HealthIncreaseRandom,
        HealthIncreaseRandomMinTwo,
        HealthIncreaseRandomRerollOnes,
        CharacterConverter,
        InitialBuilder,
        WizardLLMSpellAssigner,
        SorcererLLMSpellAssigner,
        LevelAssigner,
        WizardLevel1,
        WizardLevel3,
        WizardLevel4,
        WizardLevel5,
        WizardLevel7,
        WizardLevel8,
        WizardLevel9,
        WizardLevel11,
        WizardLevel12,
        WizardLevel13,
        WizardLevel15,
        WizardLevel16,
        WizardLevel17,
        WizardLevel18,
        WizardLevel19,
        WizardLevel20,
        WizardLevel2Abjuration,
        WizardLevel6Abjuration,
        WizardLevel10Abjuration,
        WizardLevel14Abjuration,
        WizardLevel2Bladesinging,
        WizardLevel6Bladesinging,
        WizardLevel10Bladesinging,
        WizardLevel14Bladesinging,
        WizardLevel2Chronurgy,
        WizardLevel6Chronurgy,
        WizardLevel10Chronurgy,
        WizardLevel14Chronurgy,
        WizardLevel2Conjuration,
        WizardLevel6Conjuration,
        WizardLevel10Conjuration,
        WizardLevel14Conjuration,
        WizardLevel2Divination,
        WizardLevel6Divination,
        WizardLevel10Divination,
        WizardLevel14Divination,
        WizardLevel2Enchantment,
        WizardLevel6Enchantment,
        WizardLevel10Enchantment,
        WizardLevel14Enchantment,
        WizardLevel2Evocation,
        WizardLevel6Evocation,
        WizardLevel10Evocation,
        WizardLevel14Evocation,
        WizardLevel2Graviturgy,
        WizardLevel6Graviturgy,
        WizardLevel10Graviturgy,
        WizardLevel14Graviturgy,
        WizardLevel2Illusion,
        WizardLevel6Illusion,
        WizardLevel10Illusion,
        WizardLevel14Illusion,
        WizardLevel2Necromancy,
        WizardLevel6Necromancy,
        WizardLevel10Necromancy,
        WizardLevel14Necromancy,
        WizardLevel2Scribes,
        WizardLevel6Scribes,
        WizardLevel10Scribes,
        WizardLevel14Scribes,
        WizardLevel2Transmutation,
        WizardLevel6Transmutation,
        WizardLevel10Transmutation,
        WizardLevel14Transmutation,
        WizardLevel2WarMagic,
        WizardLevel6WarMagic,
        WizardLevel10WarMagic,
        WizardLevel14WarMagic,
        SorcererLevel2,
        SorcererLevel3,
        SorcererLevel4,
        SorcererLevel5,
        SorcererLevel7,
        SorcererLevel8,
        SorcererLevel9,
        SorcererLevel10,
        SorcererLevel11,
        SorcererLevel12,
        SorcererLevel13,
        SorcererLevel15,
        SorcererLevel16,
        SorcererLevel17,
        SorcererLevel19,
        SorcererLevel20,
        SorcererLevel1AberrantMind,
        SorcererLevel6AberrantMind,
        SorcererLevel14AberrantMind,
        SorcererLevel18AberrantMind,
        SorcererLevel1ClockworkSoul,
        SorcererLevel6ClockworkSoul,
        SorcererLevel14ClockworkSoul,
        SorcererLevel18ClockworkSoul,
        SorcererLevel1DraconicBloodline,
        SorcererLevel6DraconicBloodline,
        SorcererLevel14DraconicBloodline,
        SorcererLevel18DraconicBloodline,
        SorcererLevel1DivineSoul,
        SorcererLevel6DivineSoul,
        SorcererLevel14DivineSoul,
        SorcererLevel18DivineSoul,
        SorcererLevel1LunarSorcery,
        SorcererLevel6LunarSorcery,
        SorcererLevel14LunarSorcery,
        SorcererLevel18LunarSorcery,
        SorcererLevel1ShadowMagic,
        SorcererLevel6ShadowMagic,
        SorcererLevel14ShadowMagic,
        SorcererLevel18ShadowMagic,
        SorcererLevel1StormSorcery,
        SorcererLevel6StormSorcery,
        SorcererLevel14StormSorcery,
        SorcererLevel18StormSorcery,
        SorcererLevel1WildMagic,
        SorcererLevel6WildMagic,
        SorcererLevel14WildMagic,
        SorcererLevel18WildMagic,
        MaxFirstResolver,
        MaxIfNotMaxedResolver,
        NullBlock,
        OptionalSubclassAssigner,
        PriorityStatChoiceResolver,
        AarakocraRaceAssigner,
        AasimarRaceAssigner,
        BugbearRaceAssigner,
        CentaurRaceAssigner,
        ChangelingRaceAssigner,
        DragonbornRaceAssigner,
        DwarfRaceAssigner,
        ElfRaceAssigner,
        FirbolgRaceAssigner,
        GenasiAirRaceAssigner,
        GenasiEarthRaceAssigner,
        GenasiFireRaceAssigner,
        GenasiWaterRaceAssigner,
        GnomeRaceAssigner,
        GoblinRaceAssigner,
        GoliathRaceAssigner,
        GrungRaceAssigner,
        HalfElfRaceAssigner,
        HalflingRaceAssigner,
        HalfOrcRaceAssigner,
        HobgoblinRaceAssigner,
        HumanRaceAssigner,
        KalashtarRaceAssigner,
        KenkuRaceAssigner,
        KoboldRaceAssigner,
        LeoninRaceAssigner,
        LizardfolkRaceAssigner,
        MinotaurRaceAssigner,
        OrcRaceAssigner,
        SatyrRaceAssigner,
        ShifterRaceAssigner,
        TabaxiRaceAssigner,
        TieflingRaceAssigner,
        TortleRaceAssigner,
        VerdanRaceAssigner,
        WarforgedRaceAssigner,
        YuanTiPurebloodRaceAssigner,
        RandomEquipmentChooser,
        RandomFeatChoiceResolver,
        RandomInitialDataFiller,
        RandomLanguageChoiceResolver,
        RandomMagicalItemChooser,
        RandomRaceAssigner,
        RaceAssigner,
        RandomSkillChoiceResolver,
        WizardRandomSpellAssigner,
        SorcererRandomSpellAssigner,
        RandomSubclassAssigner,
        RandomToolProficiencyChoiceResolver,
        StandardArray,
        WeaponAdder,
        AgeAssigner,
        AlignmentAssigner,
        BackgroundAssigner,
        NameAssigner,
        SexAssigner,
    ],
    Field(discriminator="type"),
]
__all__ = [
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
    "CharacterBaseTemplate",
    "CharacterDataAssigner",
    "EquipmentAdder",
    "FeatAdder",
    "FeatureAssigner",
    "HealthIncreaseAverage",
    "HealthIncreaseRandom",
    "HealthIncreaseRandomMinTwo",
    "HealthIncreaseRandomRerollOnes",
    "LevelAssigner",
    "WizardLevel1",
    "WizardLevel3",
    "WizardLevel4",
    "WizardLevel5",
    "WizardLevel7",
    "WizardLevel8",
    "WizardLevel9",
    "WizardLevel11",
    "WizardLevel12",
    "WizardLevel13",
    "WizardLevel15",
    "WizardLevel16",
    "WizardLevel17",
    "WizardLevel18",
    "WizardLevel19",
    "WizardLevel20",
    "WizardLevel2Abjuration",
    "WizardLevel6Abjuration",
    "WizardLevel10Abjuration",
    "WizardLevel14Abjuration",
    "WizardLevel2Bladesinging",
    "WizardLevel6Bladesinging",
    "WizardLevel10Bladesinging",
    "WizardLevel14Bladesinging",
    "WizardLevel2Chronurgy",
    "WizardLevel6Chronurgy",
    "WizardLevel10Chronurgy",
    "WizardLevel14Chronurgy",
    "WizardLevel2Conjuration",
    "WizardLevel6Conjuration",
    "WizardLevel10Conjuration",
    "WizardLevel14Conjuration",
    "WizardLevel2Divination",
    "WizardLevel6Divination",
    "WizardLevel10Divination",
    "WizardLevel14Divination",
    "WizardLevel2Enchantment",
    "WizardLevel6Enchantment",
    "WizardLevel10Enchantment",
    "WizardLevel14Enchantment",
    "WizardLevel2Evocation",
    "WizardLevel6Evocation",
    "WizardLevel10Evocation",
    "WizardLevel14Evocation",
    "WizardLevel2Graviturgy",
    "WizardLevel6Graviturgy",
    "WizardLevel10Graviturgy",
    "WizardLevel14Graviturgy",
    "WizardLevel2Illusion",
    "WizardLevel6Illusion",
    "WizardLevel10Illusion",
    "WizardLevel14Illusion",
    "WizardLevel2Necromancy",
    "WizardLevel6Necromancy",
    "WizardLevel10Necromancy",
    "WizardLevel14Necromancy",
    "WizardLevel2Scribes",
    "WizardLevel6Scribes",
    "WizardLevel10Scribes",
    "WizardLevel14Scribes",
    "WizardLevel2Transmutation",
    "WizardLevel6Transmutation",
    "WizardLevel10Transmutation",
    "WizardLevel14Transmutation",
    "WizardLevel2WarMagic",
    "WizardLevel6WarMagic",
    "WizardLevel10WarMagic",
    "WizardLevel14WarMagic",
    "SorcererLevel2",
    "SorcererLevel3",
    "SorcererLevel4",
    "SorcererLevel5",
    "SorcererLevel7",
    "SorcererLevel8",
    "SorcererLevel9",
    "SorcererLevel10",
    "SorcererLevel11",
    "SorcererLevel12",
    "SorcererLevel13",
    "SorcererLevel15",
    "SorcererLevel16",
    "SorcererLevel17",
    "SorcererLevel19",
    "SorcererLevel20",
    "SorcererLevel1AberrantMind",
    "SorcererLevel6AberrantMind",
    "SorcererLevel14AberrantMind",
    "SorcererLevel18AberrantMind",
    "SorcererLevel1ClockworkSoul",
    "SorcererLevel6ClockworkSoul",
    "SorcererLevel14ClockworkSoul",
    "SorcererLevel18ClockworkSoul",
    "SorcererLevel1DraconicBloodline",
    "SorcererLevel6DraconicBloodline",
    "SorcererLevel14DraconicBloodline",
    "SorcererLevel18DraconicBloodline",
    "SorcererLevel1DivineSoul",
    "SorcererLevel6DivineSoul",
    "SorcererLevel14DivineSoul",
    "SorcererLevel18DivineSoul",
    "SorcererLevel1LunarSorcery",
    "SorcererLevel6LunarSorcery",
    "SorcererLevel14LunarSorcery",
    "SorcererLevel18LunarSorcery",
    "SorcererLevel1ShadowMagic",
    "SorcererLevel6ShadowMagic",
    "SorcererLevel14ShadowMagic",
    "SorcererLevel18ShadowMagic",
    "SorcererLevel1StormSorcery",
    "SorcererLevel6StormSorcery",
    "SorcererLevel14StormSorcery",
    "SorcererLevel18StormSorcery",
    "SorcererLevel1WildMagic",
    "SorcererLevel6WildMagic",
    "SorcererLevel14WildMagic",
    "SorcererLevel18WildMagic",
    "WizardLLMSpellAssigner",
    "SorcererLLMSpellAssigner",
    "MaxFirstResolver",
    "MaxIfNotMaxedResolver",
    "CharacterConverter",
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
    "StandardArray",
    "WeaponAdder",
    "AgeAssigner",
    "AlignmentAssigner",
    "BackgroundAssigner",
    "NameAssigner",
    "SexAssigner",
    "AnyBuildingBlock",
]
