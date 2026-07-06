from __future__ import annotations

import sys


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
    SorcererLevelIncrementer,
)
from dnd.character.blueprint.building_blocks.level_up.level_up import (
    LevelUp,
)
from dnd.character.blueprint.building_blocks.level_up.level_up_multiple import (
    LevelUpMultiple,
)
from dnd.character.blueprint.building_blocks.level_up.spell_assignment import (
    SorcererRandomSpellAssigner,
)
from dnd.character.blueprint.building_blocks.level_up.spell_assignment.base import (
    SorcererSpellAssigner,
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
    SorcererSubclass,
)
from dnd.choices.stats_creation.statistic import Statistic

SpellAssigner = SorcererSpellAssigner


@pytest.mark.integration
class TestBuildSorcerer:
    STATS_PRIORITY = (
        Statistic.CHARISMA,
        Statistic.CONSTITUTION,
        Statistic.WISDOM,
        Statistic.DEXTERITY,
        Statistic.INTELLIGENCE,
        Statistic.STRENGTH,
    )
    LEVEL = 16
    RACE = Race.HUMAN
    SUBRACE = SubraceName.HUMAN_VARIANT_HUMAN_PLAYERSHANDBOOK
    CLASS = Class.SORCERER
    SUBCLASSES = (
        SorcererSubclass.DRACONIC_BLOODLINE,
        SorcererSubclass.STORM_SORCERY,
    )

    @classmethod
    def _create_level_up(
        cls,
        all_choices_resolver: AllChoicesResolverBase,
        class_: Class,
        spell_assigner: SpellAssigner,
    ) -> LevelUp:
        return LevelUp(
            blocks=(
                SorcererLevelIncrementer(),
                HealthIncreaseAverage(class_=class_),
                spell_assigner,
                all_choices_resolver,
            ),
        )

    @classmethod
    def _build_sorc(
        cls,
        magical_item_chooser: object,
        all_choices_resolver: AllChoicesResolverBase,
        initial_data_filler: InitialDataFiller,
        subclass_assigner: SubclassAssigner,
        spell_assigner: SpellAssigner,
    ) -> object:
        level_up = cls._create_level_up(
            all_choices_resolver,
            class_=cls.CLASS,
            spell_assigner=spell_assigner,
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

    def test_build_sorcerer(self) -> None:
        magical_item_chooser = RandomMagicalItemChooser(
            n_uncommon=1,
            n_rare=2,
            n_very_rare=1,
            n_legendary=1,
            seed=42,
        )
        sorcerer = self._build_sorc(
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
            SorcererRandomSpellAssigner(),
        ).character

        assert isinstance(sorcerer, Character)
        assert sorcerer.weapons
        assert sorcerer.other_equipment
        assert sorcerer.magical_items
        assert len(sorcerer.magical_items) == 5
        sys.stdout.write(
            sorcerer.model_dump_json(
                indent=2,
                exclude_defaults=True,
            )
        )
