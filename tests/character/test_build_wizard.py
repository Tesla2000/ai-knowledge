from __future__ import annotations

from collections.abc import Callable

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
    LevelIncrementer,
)
from dnd.character.blueprint.building_blocks.level_up.level_up import (
    LevelUp,
)
from dnd.character.blueprint.building_blocks.level_up.level_up_multiple import (
    LevelUpMultiple,
)
from dnd.character.blueprint.building_blocks.level_up.spell_assignment import (
    LLMSpellAssigner,
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
    AISubclassAssigner,
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
from dnd.character.race.subraces import Subrace
from dnd.choices.class_creation.character_class import Class
from dnd.choices.class_creation.character_class import (
    WizardSubclass,
)
from dnd.choices.stats_creation.statistic import Statistic
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()


@pytest.mark.integration
class TestBuildWizard:
    # Common test configuration
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
    SUBRACE = Subrace.GNOME_ROCK_GNOME_PLAYERSHANDBOOK
    CLASS = Class.WIZARD
    SUBCLASSES = (WizardSubclass.CONJURATION,)

    @classmethod
    def _create_level_up(
        cls, all_choices_resolver, class_: Class, spell_assigner: SpellAssigner
    ):
        """Create standard level up block for wizard tests."""
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
        magical_item_chooser,
        all_choices_resolver: AllChoicesResolverBase,
        initial_data_filler: InitialDataFiller,
        subclass_assigner: SubclassAssigner,
        spell_assigner_creator: Callable[[Class], SpellAssigner],
    ):
        """Build a wizard character with the specified magical item chooser.

        Args:
            magical_item_chooser: MagicalItemChooserBase instance.
            all_choices_resolver: Optional custom AllChoicesResolverBase.
                If None, uses standard random resolver.

        Returns:
            Built wizard character.
        """
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

    def test_build_wizard(self):
        """Test wizard build with random magical item selection."""
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
        assert (
            len(wizard.magical_items) == 5
        )  # 1 uncommon + 2 rare + 1 very_rare + 1 legendary
        print(
            wizard.model_dump_json(
                indent=2,
                exclude_defaults=True,
            )
        )

    @pytest.mark.requires_api_key
    def test_build_wizard_with_ai(self):
        """Test wizard build with AI-powered choices (all choices including magical items)."""
        # Create LLM for AI-powered choices
        llm = ChatOpenAI(model="gpt-5.4", temperature=0.7)
        spells_llm = ChatOpenAI(model="gpt-5.4-mini", temperature=0.3)

        # Use AI for ALL choices (languages, skills, feats, stats, magical items)
        all_choices_resolver = AIAllChoicesResolver(
            blocks=(
                PriorityStatChoiceResolver(priority=self.STATS_PRIORITY),
                RandomEquipmentChooser(),
                MaxIfNotMaxedResolver(priority=self.STATS_PRIORITY),
                AIAllNonStatChoicesResolver(llm=llm),
            )
        )

        # Use AI for magical item selection
        magical_item_chooser = AIMagicalItemChooser(
            llm=llm,
            n_uncommon=0,
            n_rare=2,
            n_very_rare=1,
            n_legendary=1,
        )
        previous_result = ""
        for character_description in (
            # "Dark lady, channeling profane power, independent of her undead minions, focuses on controll and disruptive spells, with some high damage options",
            "Mistress of evil, summer of friends, mighty and prepared with deadly spells for combat. Has Robe of archmagi in equipment",
            # "Rządna władzy czarodziejka gotowa złamać wszelkie zasady by osiągnąć cel, preferuje manipulację i magię błyskawic",
        ):
            character_description += previous_result
            result = self._build_wizard(
                magical_item_chooser,
                all_choices_resolver,
                AIPartialBuilderAssigner(
                    description=character_description,
                    llm=llm,
                ),
                AISubclassAssigner(
                    class_=self.CLASS,
                    available_subclasses=self.SUBCLASSES,
                    llm=llm,
                ),
                lambda class_: LLMSpellAssigner(
                    class_=class_,
                    llm=spells_llm,
                    character_description=character_description,
                ),
            )
            character = result.character
            assert isinstance(character, Character), result.error
            assert character.weapons
            assert character.other_equipment
            assert character.magical_items

            previous_result += (
                "You already constructed this character. Make this one a bit different holding true to the description"
                + character.model_dump_json(
                    exclude_defaults=True,
                )
            )
            print(
                character.model_dump_json(
                    indent=2,
                    exclude_defaults=True,
                )
            )
