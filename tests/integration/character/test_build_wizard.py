from __future__ import annotations

import sys

from collections.abc import Callable

import pytest
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
    RandomLanguageChoiceResolver,
)
from dnd.character.blueprint.building_blocks import (
    RandomMagicalItemChooser,
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
from dnd.character.blueprint.building_blocks.all_choices_resolver.base_resolver import (
    AllChoicesResolverBase,
)
from dnd.character.blueprint.building_blocks.equipment_chooser.random import (
    RandomEquipmentChooser,
)
from dnd.character.blueprint.building_blocks.feat_choice_resolver.max_first import (
    MaxFirstResolver,
)
from dnd.character.blueprint.building_blocks.initial_builder import (
    InitialBuilder,
)
from dnd.character.blueprint.building_blocks.initial_data_filler import (
    RandomInitialDataFiller,
)
from dnd.character.blueprint.building_blocks.initial_data_filler.base_filler import (
    InitialDataFiller,
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
from dnd.character.blueprint.building_blocks.level_up.spell_assignment.base import (
    SpellAssigner,
)
from dnd.character.blueprint.building_blocks.stats_builder.standard_array import (
    StandardArray,
)
from dnd.character.blueprint.building_blocks.subclass_assigner import (
    RandomSubclassAssigner,
)
from dnd.character.blueprint.building_blocks.subclass_assigner.base import (
    SubclassAssigner,
)
from dnd.character.builder import Builder
from dnd.character.character import Character
from dnd.character.checkpoint import MemoryStorage
from dnd.character.race.race import Race
from dnd.character.race.subraces import SubraceName
from dnd.choices.class_creation.character_class import Class
from dnd.choices.class_creation.character_class import (
    WizardSubclass,
)
from dnd.choices.stats_creation.statistic import Statistic


@pytest.mark.integration
class TestBuildWizard:
    STATS_PRIORITY = (
        Statistic.INTELLIGENCE,
        Statistic.CONSTITUTION,
        Statistic.WISDOM,
        Statistic.DEXTERITY,
        Statistic.CHARISMA,
        Statistic.STRENGTH,
    )
    LEVEL = 20
    RACE = Race.GNOME
    SUBRACE = SubraceName.GNOME_ROCK_GNOME_PLAYERSHANDBOOK
    CLASS = Class.WIZARD
    SUBCLASSES = (WizardSubclass.CONJURATION,)

    @classmethod
    def _create_level_up(
        cls,
        all_choices_resolver: AllChoicesResolverBase,
        class_: Class,
        spell_assigner: SpellAssigner,
    ) -> LevelUp:
        return LevelUp(
            blocks=(
                LevelIncrementer(class_=class_),
                HealthIncreaseAverage(class_=class_),
                spell_assigner,
                all_choices_resolver,
            ),
        )

    @classmethod
    def _build_wizard(
        cls,
        magical_item_chooser: object,
        all_choices_resolver: AllChoicesResolverBase,
        initial_data_filler: InitialDataFiller,
        subclass_assigner: SubclassAssigner,
        spell_assigner_creator: Callable[[Class], SpellAssigner],
    ) -> object:
        level_up = cls._create_level_up(
            all_choices_resolver,
            class_=cls.CLASS,
            spell_assigner=spell_assigner_creator(cls.CLASS),
        )

        builder = (
            Builder(increment_storage=MemoryStorage())
            .add(
                InitialBuilder(
                    blocks=(
                        LevelAssigner(level=cls.LEVEL),
                        StandardArray(stats_priority=cls.STATS_PRIORITY),
                        RaceAssigner(
                            race=cls.RACE,
                            subrace=cls.SUBRACE,
                        ),
                        all_choices_resolver,
                    )
                )
            )
            .add(initial_data_filler)
            .add(LevelUpMultiple(blocks=tuple(level_up for _ in range(cls.LEVEL - 1))))
            .add(subclass_assigner)
            .add(magical_item_chooser)
        )
        return builder.build()

    def test_build_wizard(self) -> None:
        magical_item_chooser = RandomMagicalItemChooser(
            n_uncommon=1,
            n_rare=2,
            n_very_rare=1,
            n_legendary=1,
            seed=42,
        )
        wizard = self._build_wizard(
            magical_item_chooser,
            AllChoicesResolver(
                blocks=(
                    RandomLanguageChoiceResolver(),
                    RandomSkillChoiceResolver(),
                    MaxFirstResolver(
                        priority=self.STATS_PRIORITY,
                        then=RandomFeatChoiceResolver(),
                    ),
                    RandomToolProficiencyChoiceResolver(),
                    PriorityStatChoiceResolver(priority=self.STATS_PRIORITY),
                    RandomEquipmentChooser(),
                ),
            ),
            RandomInitialDataFiller(),
            RandomSubclassAssigner(
                class_=self.CLASS,
                available_subclasses=self.SUBCLASSES,
            ),
            lambda class_: RandomSpellAssigner(class_=class_),
        ).character

        assert isinstance(wizard, Character)
        assert wizard.weapons
        assert wizard.other_equipment
        assert wizard.magical_items
        assert len(wizard.magical_items) == 5
        sys.stdout.write(
            wizard.model_dump_json(
                indent=2,
                exclude_defaults=True,
            )
        )
