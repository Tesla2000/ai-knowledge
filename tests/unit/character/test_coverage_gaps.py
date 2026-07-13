import random as _random_module
from unittest.mock import MagicMock

import pytest
from pydantic import create_model

from dnd.character.armor.armors import ARMORS
from dnd.character.armor.names import ArmorName
from dnd.character.blueprint.formatter import BlueprintFormatter
from dnd.character.blueprint.building_blocks.age_assigner import AgeAssigner
from dnd.character.blueprint.building_blocks.alignment_assigner import AlignmentAssigner
from dnd.character.blueprint.building_blocks.background_assigner import (
    BackgroundAssigner,
)
from dnd.character.blueprint.building_blocks.character_data_assigner import (
    CharacterDataAssigner,
)
from dnd.character.blueprint.building_blocks.character_data_field_assigner import (
    CharacterDataFieldAssigner,
)
from dnd.character.blueprint.building_blocks.equipment_chooser.ai import (
    AIEquipmentChooser,
)
from dnd.character.blueprint.building_blocks.feat_choice_resolver.base import (
    FeatChoiceResolver,
)
from dnd.character.blueprint.building_blocks.feat_choice_resolver.max_first import (
    MaxFirstResolver,
)
from dnd.character.blueprint.building_blocks.feat_choice_resolver.random import (
    RandomFeatChoiceResolver,
)
from dnd.character.blueprint.building_blocks.initial_data_filler.base_filler import (
    InitialDataFiller,
)
from dnd.character.blueprint.building_blocks.language_choice_resolver.base import (
    LanguageChoiceResolver,
)
from dnd.character.blueprint.building_blocks.language_choice_resolver.random import (
    RandomLanguageChoiceResolver,
)
from dnd.character.blueprint.building_blocks.level_assigner import LevelAssigner
from dnd.character.blueprint.building_blocks.level_up.health_increase.base import (
    HealthIncrease,
)
from dnd.character.blueprint.building_blocks.level_up.health_increase.random_reroll_ones import (
    HealthIncreaseRandomRerollOnes,
)
from dnd.character.blueprint.building_blocks.level_up.spell_assignment.base import (
    WizardSpellAssigner,
    SorcererSpellAssigner,
    SpellSelector,
)
from dnd.character.spells import Spell
from dnd.character.blueprint.building_blocks.level_up.spell_assignment import (
    SorcererRandomSpellAssigner,
    WizardRandomSpellAssigner,
)
from dnd.character.blueprint.building_blocks.initial_data_filler.random_filler import (
    RandomInitialDataFiller,
)
from dnd.character.blueprint.building_blocks.magical_item_chooser.base_chooser import (
    MagicalItemChooserBase,
)
from dnd.character.blueprint.building_blocks.magical_item_chooser.random import (
    RandomMagicalItemChooser,
)
from dnd.character.blueprint.building_blocks.name_assigner import NameAssigner
from dnd.character.blueprint.building_blocks.race_assigner.base_race_assigner import (
    BaseRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner.base_race_assigner import (
    RaceSubracePair,
)
from dnd.character.blueprint.building_blocks.race_assigner.race_assigner import (
    RaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner.race_assigner import (
    HumanRaceAssigner,
)
from dnd.character.blueprint.building_blocks.sex_assigner import SexAssigner
from dnd.character.blueprint.building_blocks.skill_choice_resolver.ai import (
    AISkillChoiceResolver,
    SkillSelection,
)
from dnd.character.blueprint.building_blocks.skill_choice_resolver.base import (
    SkillChoiceResolver,
)
from dnd.character.blueprint.building_blocks.skill_choice_resolver.random import (
    RandomSkillChoiceResolver,
)
from dnd.character.blueprint.building_blocks.stat_choice_resolver.base import (
    StatChoiceResolver,
)
from dnd.character.blueprint.building_blocks.stat_choice_resolver.priority import (
    PriorityStatChoiceResolver,
)
from dnd.character.blueprint.building_blocks.stats_builder.standard_array import (
    StandardArray,
)
from dnd.character.blueprint.building_blocks.stats_priority import StatsPriority
from dnd.character.blueprint.building_blocks.subclass_assigner.ai import (
    AISubclassAssigner,
)
from dnd.character.blueprint.building_blocks.subclass_assigner.random import (
    RandomSubclassAssigner,
)
from dnd.character.blueprint.building_blocks.subclass_assigner.subclass_assigner import (
    WizardSubclassAssigner,
)
from dnd.character.blueprint.building_blocks.tool_proficiency_choice_resolver.base import (
    ToolProficiencyChoiceResolver,
)
from dnd.character.blueprint.building_blocks.tool_proficiency_choice_resolver.random import (
    RandomToolProficiencyChoiceResolver,
)
from dnd.character.blueprint.character_data import CharacterData
from dnd.character.blueprint.states.state import Blueprint
from dnd.character.class_levels import ClassLevels
from dnd.character.magical_item.items import robe_of_the_archmagi
from dnd.character.race.race import Race
from dnd.character.race.subraces import SubraceName
from dnd.character.stats import Stats
from dnd.choices.alignment import Alignment
from dnd.choices.background_creatrion.background import Background
from dnd.choices.class_creation.character_class import (
    Class,
    WizardSubclass,
    SorcererSubclass,
)
from dnd.choices.equipment_creation.weapons import HitDieSize, WeaponName
from dnd.choices.sex import Sex
from dnd.choices.stats_creation.statistic import Statistic
from dnd.other_profficiencies import ArmorProficiency
from dnd.skill_proficiency import Skill
import dnd.fight._creature as creature_module

_PRIORITY: StatsPriority = (
    Statistic.STRENGTH,
    Statistic.DEXTERITY,
    Statistic.CONSTITUTION,
    Statistic.INTELLIGENCE,
    Statistic.WISDOM,
    Statistic.CHARISMA,
)

_DEFAULT_STATS = Stats(
    strength=10, dexterity=10, constitution=10, intelligence=10, wisdom=10, charisma=10
)


@pytest.mark.unit
class TestCharacterDataFieldAssigners:
    def test_age_assigner_apply(self) -> None:
        assigner = AgeAssigner(age=25)
        result = assigner.apply(Blueprint())
        assert result.character_data is not None
        assert result.character_data.age == 25

    def test_alignment_assigner_apply(self) -> None:
        assigner = AlignmentAssigner(alignment=Alignment.CHAOTIC_GOOD)
        result = assigner.apply(Blueprint())
        assert result.character_data is not None
        assert result.character_data.alignment == Alignment.CHAOTIC_GOOD

    def test_background_assigner_apply(self) -> None:
        assigner = BackgroundAssigner(background=Background.SAGE)
        result = assigner.apply(Blueprint())
        assert result.character_data is not None
        assert result.character_data.background == Background.SAGE

    def test_name_assigner_apply(self) -> None:
        assigner = NameAssigner(name="Gandalf")
        result = assigner.apply(Blueprint())
        assert result.character_data is not None
        assert result.character_data.name == "Gandalf"

    def test_sex_assigner_apply(self) -> None:
        assigner = SexAssigner(sex=Sex.FEMALE)
        result = assigner.apply(Blueprint())
        assert result.character_data is not None
        assert result.character_data.sex == Sex.FEMALE

    def test_character_data_assigner_apply(self) -> None:
        cd = CharacterData(name="Gandalf")
        assigner = CharacterDataAssigner(character_data=cd)
        result = assigner.apply(Blueprint())
        assert result.character_data == cd

    def test_abstract_update_body(self) -> None:
        assigner = AgeAssigner(age=5)
        result = CharacterDataFieldAssigner._update(assigner, CharacterData())
        assert result is None


@pytest.mark.unit
class TestArmorCalcAC:
    def _make_state(
        self,
        race: Race = Race.HUMAN,
        proficiencies: tuple[ArmorProficiency, ...] = (),
        classes: ClassLevels | None = None,
    ) -> Blueprint:
        state = Blueprint(stats=_DEFAULT_STATS)
        state = state.model_copy(
            update={
                "race": race,
                "armor_proficiencies": frozenset(proficiencies),
                "classes": classes or ClassLevels(),
            }
        )
        return state

    def test_heavy_armor_with_proficiency(self) -> None:
        armor = ARMORS[ArmorName.CHAIN_MAIL]
        state = self._make_state(proficiencies=(ArmorProficiency.HEAVY_ARMOR,))
        ac = armor.calc_ac(state)
        assert ac == armor.base_ac

    def test_medium_armor_with_proficiency(self) -> None:
        armor = ARMORS[ArmorName.BREASTPLATE]
        state = self._make_state(proficiencies=(ArmorProficiency.MEDIUM_ARMOR,))
        ac = armor.calc_ac(state)
        assert ac == armor.base_ac + min(
            2, _DEFAULT_STATS.get_modifier(Statistic.DEXTERITY)
        )

    def test_monk_wisdom_bonus(self) -> None:
        armor = ARMORS[ArmorName.CLOTHES]
        state = self._make_state(classes=ClassLevels(monk=1))
        ac = armor.calc_ac(state)
        dex_mod = _DEFAULT_STATS.get_modifier(Statistic.DEXTERITY)
        wis_mod = _DEFAULT_STATS.get_modifier(Statistic.WISDOM)
        assert ac == armor.base_ac + dex_mod + wis_mod

    def test_barbarian_constitution_bonus(self) -> None:
        armor = ARMORS[ArmorName.CLOTHES]
        state = self._make_state(classes=ClassLevels(barbarian=1))
        ac = armor.calc_ac(state)
        dex_mod = _DEFAULT_STATS.get_modifier(Statistic.DEXTERITY)
        con_mod = _DEFAULT_STATS.get_modifier(Statistic.CONSTITUTION)
        assert ac == armor.base_ac + dex_mod + con_mod

    def test_lizardfolk_natural_ac(self) -> None:
        armor = ARMORS[ArmorName.CLOTHES]
        state = self._make_state(race=Race.LIZARDFOLK)
        ac = armor.calc_ac(state)
        dex_mod = _DEFAULT_STATS.get_modifier(Statistic.DEXTERITY)
        assert ac == max(armor.base_ac + dex_mod, 13 + dex_mod)


@pytest.mark.unit
class TestClassLevelsGetItem:
    def test_getitem_returns_level(self) -> None:
        levels = ClassLevels(wizard=3)
        assert levels[Class.WIZARD] == 3

    def test_getitem_zero_for_absent_class(self) -> None:
        levels = ClassLevels()
        assert levels[Class.SORCERER] == 0


@pytest.mark.unit
class TestRobeOfTheArchmagiCalcAC:
    def test_calc_ac_returns_base_plus_dex(self) -> None:
        robe = robe_of_the_archmagi
        state = Blueprint(stats=_DEFAULT_STATS)
        ac = robe.calc_ac(state)
        assert ac == robe.base_ac + _DEFAULT_STATS.get_modifier(Statistic.DEXTERITY)


@pytest.mark.unit
class TestRaceAssignerGetRaceAndSubrace:
    def test_returns_correct_pair(self) -> None:
        assigner = RaceAssigner(
            race=Race.HUMAN,
            subrace=SubraceName.HUMAN_STANDARD_HUMAN_PLAYERSHANDBOOK,
        )
        pair = assigner._get_race_and_subrace()
        assert pair == RaceSubracePair(
            race=Race.HUMAN,
            subrace=SubraceName.HUMAN_STANDARD_HUMAN_PLAYERSHANDBOOK,
        )

    def test_base_abstract_body(self) -> None:
        assigner = HumanRaceAssigner(
            subrace=SubraceName.HUMAN_STANDARD_HUMAN_PLAYERSHANDBOOK
        )
        result = BaseRaceAssigner._get_race_and_subrace(assigner)
        assert result is None


@pytest.mark.unit
class TestMaxFirstResolverFallback:
    def test_falls_back_to_then_at_level_1(self) -> None:
        state = LevelAssigner(level=1).apply(Blueprint())
        state = StandardArray(stats_priority=_PRIORITY).apply(state)
        state = state.model_copy(update={"classes": ClassLevels(wizard=1)})
        resolver = MaxFirstResolver(
            priority=_PRIORITY, then=RandomFeatChoiceResolver(seed=42)
        )
        result = resolver.apply(state)
        assert result is not None

    def test_abstract_select_from_available_body(self) -> None:
        resolver = RandomFeatChoiceResolver(seed=42)
        result = FeatChoiceResolver._select_from_available(
            resolver, [], _DEFAULT_STATS, _DEFAULT_STATS
        )
        assert result is None


@pytest.mark.unit
class TestPriorityStatChoiceResolverSecondaryLoop:
    def test_secondary_loop_distributes_remaining(self) -> None:
        high_stats = Stats(
            strength=15,
            dexterity=15,
            constitution=15,
            intelligence=15,
            wisdom=15,
            charisma=15,
        )
        BlueprintWithChoices = create_model(
            "BlueprintHighStats",
            stats=(Stats, ...),
            n_stat_choices=(int, ...),
            __base__=Blueprint,
        )
        state = BlueprintWithChoices(stats=high_stats, n_stat_choices=1)
        resolver = PriorityStatChoiceResolver(priority=_PRIORITY)
        result = resolver.select_stats_to_increase(state)
        assert sum(result.values()) == 1

    def test_secondary_loop_skips_capped_stat(self) -> None:
        capped_stats = Stats(
            strength=20,
            dexterity=15,
            constitution=15,
            intelligence=15,
            wisdom=15,
            charisma=15,
        )
        BlueprintWithChoices = create_model(
            "BlueprintCappedStats",
            stats=(Stats, ...),
            n_stat_choices=(int, ...),
            __base__=Blueprint,
        )
        state = BlueprintWithChoices(stats=capped_stats, n_stat_choices=1)
        resolver = PriorityStatChoiceResolver(priority=_PRIORITY)
        result = resolver.select_stats_to_increase(state)
        assert result.get(Statistic.STRENGTH, 0) == 0
        assert sum(result.values()) == 1

    def test_secondary_loop_all_capped(self) -> None:
        all_capped = Stats(
            strength=20,
            dexterity=20,
            constitution=20,
            intelligence=20,
            wisdom=20,
            charisma=20,
        )
        BlueprintWithChoices = create_model(
            "BlueprintAllCapped",
            stats=(Stats, ...),
            n_stat_choices=(int, ...),
            __base__=Blueprint,
        )
        state = BlueprintWithChoices(stats=all_capped, n_stat_choices=1)
        resolver = PriorityStatChoiceResolver(priority=_PRIORITY)
        result = resolver.select_stats_to_increase(state)
        assert sum(result.values()) == 0

    def test_abstract_select_stats_body(self) -> None:
        resolver = PriorityStatChoiceResolver(priority=_PRIORITY)
        result = StatChoiceResolver.select_stats_to_increase(resolver, Blueprint())
        assert result is None


@pytest.mark.unit
class TestAISkillChoiceResolverWithCharacterDescription:
    def test_character_description_added_to_prompt(self) -> None:
        mock_llm = MagicMock()
        mock_llm.create_structured_output.return_value = SkillSelection(
            selected_skills=(Skill.ARCANA,)
        )
        block = AISkillChoiceResolver.model_construct(
            llm=mock_llm, formatter=BlueprintFormatter()
        )
        state = Blueprint(
            race=Race.HUMAN,
            n_skill_choices=1,
            skills_to_choose_from=frozenset({Skill.ARCANA, Skill.HISTORY}),
        )
        result = block.apply(state)
        assert result is not None
        mock_llm.create_structured_output.assert_called_once()

    def test_abstract_select_skills_body(self) -> None:
        resolver = RandomSkillChoiceResolver()
        result = SkillChoiceResolver._select_skills(resolver, Blueprint())
        assert result is None


@pytest.mark.unit
class TestAIEquipmentChooserWithCharacterDescription:
    def test_character_description_added_to_prompt(self) -> None:
        mock_llm = MagicMock()
        mock_llm.create_structured_output.side_effect = lambda prompt, model_class: (
            model_class(choice_0=0)
        )
        block = AIEquipmentChooser.model_construct(
            llm=mock_llm, formatter=BlueprintFormatter()
        )
        state = Blueprint(
            race=Race.HUMAN,
            equipment_choices=((WeaponName.DAGGER,),),
        )
        result = block.apply(state)
        assert result is not None
        mock_llm.create_structured_output.assert_called_once()

    def test_build_prompt_with_no_equipment_choices(self) -> None:
        block = AIEquipmentChooser.model_construct(
            llm=MagicMock(), formatter=BlueprintFormatter()
        )
        result = block._build_prompt(Blueprint())
        assert "Selection Instructions" not in result


@pytest.mark.unit
class TestAbstractMethodBodies:
    def test_language_choice_resolver_abstract_body(self) -> None:
        resolver = RandomLanguageChoiceResolver()
        result = LanguageChoiceResolver._select_from_available(resolver, [], ())
        assert result is None

    def test_health_increase_abstract_body(self) -> None:
        block = HealthIncreaseRandomRerollOnes(class_=Class.WIZARD)
        result = HealthIncrease._get_hit_die_value(block, HitDieSize.SIX)
        assert result is None

    def test_initial_data_filler_abstract_body(self) -> None:
        filler = RandomInitialDataFiller()
        result = InitialDataFiller.compute_character_data(filler, Blueprint())
        assert result is None

    def test_magical_item_chooser_abstract_body(self) -> None:
        chooser = RandomMagicalItemChooser()
        result = MagicalItemChooserBase.select_items(chooser, Blueprint())
        assert result is None

    def test_wizard_spell_assigner_abstract_body(self) -> None:
        assigner = WizardRandomSpellAssigner()
        result = WizardSpellAssigner.select_spells(assigner, 0, 1, [], Blueprint())
        assert result is None

    def test_sorcerer_spell_assigner_abstract_body(self) -> None:
        assigner = SorcererRandomSpellAssigner()
        result = SorcererSpellAssigner.select_spells(assigner, 0, 1, [], Blueprint())
        assert result is None

    def test_tool_proficiency_abstract_bodies(self) -> None:
        resolver = RandomToolProficiencyChoiceResolver()
        r1 = ToolProficiencyChoiceResolver.select_tool_proficiency(resolver, [], ())
        r2 = ToolProficiencyChoiceResolver.select_gaming_set(resolver, [], ())
        r3 = ToolProficiencyChoiceResolver.select_musical_instrument(resolver, [], ())
        assert r1 is None
        assert r2 is None
        assert r3 is None


@pytest.mark.unit
class TestSubclassAssignerLoopContinue:
    def test_for_loop_skips_different_class_subclass(self) -> None:
        state = Blueprint()
        state = LevelAssigner(level=3).apply(state)
        state = state.model_copy(
            update={
                "classes": ClassLevels(wizard=3, sorcerer=3),
                "subclasses": (SorcererSubclass.WILD_MAGIC,),
            }
        )
        assigner = WizardSubclassAssigner(subclass=WizardSubclass.EVOCATION)
        result = assigner.apply(state)
        assert WizardSubclass.EVOCATION in result.subclasses

    def test_random_subclass_skips_different_class_subclass(self) -> None:
        state = Blueprint()
        state = LevelAssigner(level=3).apply(state)
        state = state.model_copy(
            update={
                "classes": ClassLevels(wizard=3, sorcerer=3),
                "subclasses": (SorcererSubclass.WILD_MAGIC,),
            }
        )
        assigner = RandomSubclassAssigner(class_=Class.WIZARD, seed=42)
        result = assigner.apply(state)
        assert any(isinstance(s, WizardSubclass) for s in result.subclasses)


@pytest.mark.unit
class TestHealthIncreaseRerollOnesNoReroll:
    def test_roll_not_one_skips_reroll(self, monkeypatch: pytest.MonkeyPatch) -> None:
        block = HealthIncreaseRandomRerollOnes(class_=Class.WIZARD)
        state = Blueprint()
        state = block.apply(state)
        roll_values = iter([4])
        monkeypatch.setattr(_random_module, "randint", lambda a, b: next(roll_values))
        state = block.apply(state)
        assert state.health_base > 0


@pytest.mark.unit
class TestFightCreatureDefaultHpNoStats:
    def test_default_hp_with_no_stats(self) -> None:
        hp = creature_module._default_hp({})
        assert hp > 0


@pytest.mark.unit
class TestSpellSelectorProtocolBody:
    def test_select_protocol_body(self) -> None:
        class _ConcreteSelector:
            def select(
                self, spell_level: int, count: int, available: list[Spell]
            ) -> tuple[Spell, ...]:
                return ()

        spells: list[Spell] = []
        instance = _ConcreteSelector()
        result = SpellSelector.select(instance, 1, 1, spells)
        assert result is None


@pytest.mark.unit
class TestAISubclassAssignerLoopContinue:
    def test_loop_skips_different_class_subclass(self) -> None:
        mock_llm = MagicMock()
        mock_llm.create_structured_output.return_value = MagicMock(
            subclass=WizardSubclass.EVOCATION
        )
        state = Blueprint()
        state = state.model_copy(
            update={
                "classes": ClassLevels(wizard=3, sorcerer=1),
                "subclasses": (SorcererSubclass.WILD_MAGIC,),
            }
        )
        assigner = AISubclassAssigner.model_construct(
            class_=Class.WIZARD, llm=mock_llm, formatter=BlueprintFormatter()
        )
        result = assigner.apply(state)
        assert any(isinstance(s, WizardSubclass) for s in result.subclasses)
