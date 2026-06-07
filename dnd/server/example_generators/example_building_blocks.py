from dnd.character.blueprint.building_blocks import (
    CombinedBlock,
)
from dnd.character.blueprint.building_blocks import (
    LevelAssigner,
)
from dnd.character.blueprint.building_blocks import (
    PriorityStatChoiceResolver,
)
from dnd.character.blueprint.building_blocks import (
    RaceAssigner,
)
from dnd.character.blueprint.building_blocks import (
    RandomFeatChoiceResolver,
)
from dnd.character.blueprint.building_blocks import (
    RandomInitialDataFiller,
)
from dnd.character.blueprint.building_blocks import (
    RandomLanguageChoiceResolver,
)
from dnd.character.blueprint.building_blocks import (
    RandomSkillChoiceResolver,
)
from dnd.character.blueprint.building_blocks import (
    RandomToolProficiencyChoiceResolver,
)
from dnd.character.blueprint.building_blocks.all_choices_resolver import (
    AllChoicesResolver,
)
from dnd.character.blueprint.building_blocks.equipment_chooser import (
    RandomEquipmentChooser,
)
from dnd.character.blueprint.building_blocks.feat_choice_resolver.max_first import (
    MaxFirstResolver,
)
from dnd.character.blueprint.building_blocks.initial_builder import (
    InitialBuilder,
)
from dnd.character.blueprint.building_blocks.level_up.health_increase import (
    HealthIncreaseAverage,
)
from dnd.character.blueprint.building_blocks.level_up.level_incrementer import (
    LevelIncrementer,
)
from dnd.character.blueprint.building_blocks.level_up.level_up import (
    LevelUp,
)
from dnd.character.blueprint.building_blocks.level_up.level_up_multiple import (
    LevelUpMultiple,
)
from dnd.character.blueprint.building_blocks.level_up.spell_assignment import (
    RandomSpellAssigner,
)
from dnd.character.blueprint.building_blocks.stats_builder.standard_array import (
    StandardArray,
)
from dnd.character.blueprint.building_blocks.subclass_assigner import (
    RandomSubclassAssigner,
)
from dnd.character.race.race import Race
from dnd.character.race.subraces import Subrace
from dnd.choices.class_creation.character_class import Class
from dnd.choices.stats_creation.statistic import Statistic


def example_building_blocks():
    stats_priority = (
        Statistic.INTELLIGENCE,
        Statistic.CONSTITUTION,
        Statistic.WISDOM,
        Statistic.DEXTERITY,
        Statistic.CHARISMA,
        Statistic.STRENGTH,
    )
    class_ = Class.WIZARD
    all_choices_resolver = AllChoicesResolver(
        blocks=(
            RandomLanguageChoiceResolver(),
            RandomSkillChoiceResolver(),
            MaxFirstResolver(
                priority=stats_priority,
                then=RandomFeatChoiceResolver(),
            ),
            RandomToolProficiencyChoiceResolver(),
            PriorityStatChoiceResolver(priority=stats_priority),
            RandomEquipmentChooser(),
        ),
    )
    spell_assigner = RandomSpellAssigner(class_=class_)
    level_up = LevelUp(
        blocks=(
            LevelIncrementer(class_=class_),
            HealthIncreaseAverage(class_=class_),
            spell_assigner,
            all_choices_resolver,
        ),
    )
    level = 16
    return CombinedBlock(
        blocks=(
            InitialBuilder(
                blocks=(
                    LevelAssigner(level=level),
                    StandardArray(stats_priority=stats_priority),
                    RaceAssigner(
                        race=Race.HUMAN,
                        subrace=Subrace.HUMAN_VARIANT_HUMAN_PLAYERSHANDBOOK,
                    ),
                    AllChoicesResolver(
                        blocks=(
                            RandomLanguageChoiceResolver(),
                            RandomSkillChoiceResolver(),
                            MaxFirstResolver(
                                priority=stats_priority,
                                then=RandomFeatChoiceResolver(),
                            ),
                            RandomToolProficiencyChoiceResolver(),
                            PriorityStatChoiceResolver(
                                priority=stats_priority
                            ),
                            RandomEquipmentChooser(),
                        ),
                    ),
                )
            ),
            RandomInitialDataFiller(),
            LevelUpMultiple(blocks=tuple(level_up for _ in range(level))),
            RandomSubclassAssigner(
                class_=class_,
            ),
        )
    )
