from __future__ import annotations

import sys


import pytest
from dnd.character.blueprint.building_blocks import (
    AIMagicalItemChooser,
)
from dnd.character.blueprint.building_blocks import (
    AIPartialBuilderAssigner,
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
    AIAllChoicesResolver,
)
from dnd.character.blueprint.building_blocks.all_choices_resolver import (
    AllChoicesResolver,
)
from dnd.character.blueprint.building_blocks.all_choices_resolver.ai import (
    AIAllNonStatChoicesResolver,
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
from dnd.character.blueprint.building_blocks.feat_choice_resolver.max_if_not_maxed import (
    MaxIfNotMaxedResolver,
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
    SorcererRandomSpellAssigner,
    WizardLLMSpellAssigner,
    WizardRandomSpellAssigner,
)
from dnd.character.blueprint.building_blocks.level_up.spell_assignment.base import (
    SorcererSpellAssigner,
    WizardSpellAssigner,
)
from dnd.character.blueprint.building_blocks.stats_builder.standard_array import (
    StandardArray,
)
from dnd.character.blueprint.building_blocks.subclass_assigner import (
    AISubclassAssigner,
)
from dnd.character.blueprint.building_blocks.subclass_assigner import (
    RandomSubclassAssigner,
)
from dnd.character.blueprint.building_blocks.subclass_assigner.base import (
    SubclassAssigner,
)
from dnd.character.builder import Builder
from dnd.character.builder import SuccessBuiltResult
from dnd.character.character import Character
from dnd.character.checkpoint import MemoryStorage
from dnd.character.race.race import Race
from dnd.character.race.subraces import SubraceName
from dnd.choices.class_creation.character_class import Class
from dnd.choices.class_creation.character_class import (
    SorcererSubclass,
)
from dnd.choices.stats_creation.statistic import Statistic
from dotenv import load_dotenv
from structured_output_creator import OpenAIService, RaisingService


SpellAssigner = WizardSpellAssigner | SorcererSpellAssigner
load_dotenv()


@pytest.mark.integration
class TestBuildMulticlass:
    # Common test configuration
    STATS_PRIORITY = (
        Statistic.INTELLIGENCE,
        Statistic.CONSTITUTION,
        Statistic.WISDOM,
        Statistic.DEXTERITY,
        Statistic.CHARISMA,
        Statistic.STRENGTH,
    )
    LEVEL = 16
    SORC_LEVEL = 6
    RACE = Race.HUMAN
    SUBRACE = SubraceName.HUMAN_VARIANT_HUMAN_PLAYERSHANDBOOK
    WIZARD_CLASS = Class.WIZARD
    SORC_CLASS = Class.SORCERER
    sorc_subclasses = (
        SorcererSubclass.DRACONIC_BLOODLINE,
        SorcererSubclass.STORM_SORCERY,
    )

    @classmethod
    def _create_level_up(
        cls, all_choices_resolver, class_: Class, spell_assigner: SpellAssigner
    ):
        """Create standard level up block for wizard tests."""
        return LevelUp(
            level_increment=WizardLevelIncrementer()
            if class_ == Class.WIZARD
            else SorcererLevelIncrementer(),
            health_increase=HealthIncreaseAverage(class_=class_),
            spell_assigner=spell_assigner,
            all_choice_resolver=all_choices_resolver,
        )

    @classmethod
    def _build_multiclass(
        cls,
        magical_item_chooser,
        all_choices_resolver: AllChoicesResolverBase,
        initial_data_filler: InitialDataFiller,
        wiz_subclass_assigner: SubclassAssigner,
        sorc_subclass_assigner: SubclassAssigner,
        wizard_spell_assigner: SpellAssigner,
        sorc_spell_assigner: SpellAssigner,
    ):
        """Build a wizard character with the specified magical item chooser.

        Args:
            magical_item_chooser: MagicalItemChooserBase instance.
            all_choices_resolver: Optional custom AllChoicesResolverBase.
                If None, uses standard random resolver.

        Returns:
            Built wizard character.
        """
        level_up_wizard = cls._create_level_up(
            all_choices_resolver,
            class_=Class.WIZARD,
            spell_assigner=wizard_spell_assigner,
        )
        level_up_sorc = cls._create_level_up(
            all_choices_resolver,
            class_=Class.SORCERER,
            spell_assigner=sorc_spell_assigner,
        )

        builder = (
            Builder(increment_storage=MemoryStorage())
            .add(
                InitialBuilder(
                    level_assigner=LevelAssigner(level=cls.LEVEL),
                    stats_builder=StandardArray(stats_priority=cls.STATS_PRIORITY),
                    race_assigner=RaceAssigner(
                        race=cls.RACE,
                        subrace=cls.SUBRACE,
                    ),
                    all_choices_resolver=all_choices_resolver,
                )
            )
            .add(initial_data_filler)
            .add(
                LevelUpMultiple(
                    blocks=tuple(
                        level_up_wizard for _ in range(cls.LEVEL - cls.SORC_LEVEL - 1)
                    )
                )
            )
            .add(
                LevelUpMultiple(
                    blocks=tuple(level_up_sorc for _ in range(cls.SORC_LEVEL))
                )
            )
            .add(wiz_subclass_assigner)
            .add(sorc_subclass_assigner)
            .add(magical_item_chooser)
        )
        return builder.build()

    def test_build_multiclass(self):
        """Test wizard build with random magical item selection."""
        magical_item_chooser = RandomMagicalItemChooser(
            n_uncommon=1,
            n_rare=2,
            n_very_rare=1,
            n_legendary=1,
            seed=42,
        )
        result = self._build_multiclass(
            magical_item_chooser,
            AllChoicesResolver(
                language_choice_resolver=RandomLanguageChoiceResolver(),
                skill_choice_resolver=RandomSkillChoiceResolver(),
                feat_choice_resolver=MaxFirstResolver(
                    priority=self.STATS_PRIORITY,
                    then=RandomFeatChoiceResolver(),
                ),
                tool_proficiency_choice_resolver=RandomToolProficiencyChoiceResolver(),
                stat_choice_resolver=PriorityStatChoiceResolver(
                    priority=self.STATS_PRIORITY
                ),
                equipment_chooser=RandomEquipmentChooser(),
            ),
            RandomInitialDataFiller(),
            RandomSubclassAssigner(class_=self.WIZARD_CLASS),
            RandomSubclassAssigner(
                class_=self.SORC_CLASS,
                available_subclasses=self.sorc_subclasses,
            ),
            WizardRandomSpellAssigner(),
            SorcererRandomSpellAssigner(),
        )
        assert isinstance(result, SuccessBuiltResult), result
        wizard = result.character
        assert isinstance(wizard, Character)
        assert wizard.weapons
        assert wizard.other_equipment
        assert wizard.magical_items
        assert (
            len(wizard.magical_items) == 5
        )  # 1 uncommon + 2 rare + 1 very_rare + 1 legendary
        sys.stdout.write(
            wizard.model_dump_json(
                indent=2,
                exclude_defaults=True,
            )
        )

    @pytest.mark.smoke
    def test_build_multiclass_with_ai(self):
        """Test wizard build with AI-powered choices (all choices including magical items)."""
        # Create LLM for AI-powered choices
        llm = RaisingService(service=OpenAIService(model="gpt-4o", temperature=0.7))
        spells_llm = RaisingService(
            service=OpenAIService(model="gpt-4o-mini", temperature=0.3)
        )

        # Use AI for ALL choices (languages, skills, feats, stats, magical items)
        all_choices_resolver = AIAllChoicesResolver(
            stat_choice_resolver=PriorityStatChoiceResolver(
                priority=self.STATS_PRIORITY
            ),
            equipment_chooser=RandomEquipmentChooser(),
            feat_choice_resolver=MaxIfNotMaxedResolver(priority=self.STATS_PRIORITY),
            all_non_stat_choices_resolver=AIAllNonStatChoicesResolver(llm=llm),
        )

        # Use AI for magical item selection
        magical_item_chooser = AIMagicalItemChooser(
            llm=llm,
            n_uncommon=1,
            n_rare=2,
            n_very_rare=1,
            n_legendary=1,
        )
        character_description = "Gwałtowna jak burza magini o wielkiej sile rażenia, z precyzją pozbywa się swoich wrogów, używając błyskawic"
        # character_description = "Rządna władzy czarodziejka gotowa złamać wszelkie zasady by osiągnąć cel, preferuje manipulację i magię błyskawic"
        wizard = self._build_multiclass(
            magical_item_chooser,
            all_choices_resolver,
            AIPartialBuilderAssigner(
                description=character_description,
                llm=llm,
            ),
            AISubclassAssigner(
                class_=self.WIZARD_CLASS,
                llm=llm,
            ),
            AISubclassAssigner(
                class_=self.SORC_CLASS,
                available_subclasses=self.sorc_subclasses,
                llm=llm,
            ),
            WizardLLMSpellAssigner(
                llm=spells_llm,
                character_description=character_description,
            ),
            SorcererLLMSpellAssigner(
                llm=spells_llm,
                character_description=character_description,
            ),
        ).character

        assert isinstance(wizard, Character)
        assert wizard.weapons
        assert wizard.other_equipment
        assert wizard.magical_items
        sys.stdout.write(
            wizard.model_dump_json(
                indent=2,
                exclude_defaults=True,
            )
        )
