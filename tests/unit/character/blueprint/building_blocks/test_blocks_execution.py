from __future__ import annotations

from collections.abc import Generator
from collections.abc import Iterator

import pytest

from dnd.character.blueprint.building_blocks.age_assigner import AgeAssigner
from dnd.character.blueprint.building_blocks.alignment_assigner import AlignmentAssigner
from dnd.character.blueprint.building_blocks.all_choices_resolver.base import (
    AllChoicesResolver,
)
from dnd.character.blueprint.building_blocks.background_assigner import (
    BackgroundAssigner,
)
from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)
from dnd.character.blueprint.building_blocks.equipment_adder import EquipmentAdder
from dnd.character.blueprint.building_blocks.equipment_chooser.random import (
    RandomEquipmentChooser,
)
from dnd.character.blueprint.building_blocks.feat_adder import FeatAdder
from dnd.character.blueprint.building_blocks.feat_choice_resolver.max_first import (
    MaxFirstResolver,
)
from dnd.character.blueprint.building_blocks.feat_choice_resolver.max_if_not_maxed import (
    MaxIfNotMaxedResolver,
)
from dnd.character.blueprint.building_blocks.feat_choice_resolver.random import (
    RandomFeatChoiceResolver,
)
from dnd.character.blueprint.building_blocks.feature_assigner import FeatureAssigner
from dnd.character.blueprint.building_blocks.initial_builder import InitialBuilder
from dnd.character.blueprint.building_blocks.language_choice_resolver.random import (
    RandomLanguageChoiceResolver,
)
from dnd.character.blueprint.building_blocks.level_up.health_increase.average import (
    HealthIncreaseAverage,
)
from dnd.character.blueprint.building_blocks.level_up.level_incrementer import (
    WizardLevelIncrementer,
)
from dnd.character.blueprint.building_blocks.level_up.level_up import LevelUp
from dnd.character.blueprint.building_blocks.level_up.level_up_multiple import (
    LevelUpMultiple,
)
from dnd.character.blueprint.building_blocks.level_up.spell_assignment.random import (
    SorcererRandomSpellAssigner,
    WizardRandomSpellAssigner,
)
from dnd.character.blueprint.building_blocks.magical_item_chooser.random import (
    RandomMagicalItemChooser,
)
from dnd.character.blueprint.building_blocks.name_assigner import NameAssigner
from dnd.character.blueprint.building_blocks.null_block import NullBlock
from dnd.character.blueprint.building_blocks.race_assigner.race_assigner import (
    HumanRaceAssigner,
)
from dnd.character.blueprint.building_blocks.sex_assigner import SexAssigner
from dnd.character.blueprint.building_blocks.skill_choice_resolver.random import (
    RandomSkillChoiceResolver,
)
from dnd.character.blueprint.building_blocks.stat_choice_resolver.priority import (
    PriorityStatChoiceResolver,
)
from dnd.character.blueprint.building_blocks.stats_priority import StatsPriority
from dnd.character.blueprint.building_blocks.subclass_assigner.optional import (
    OptionalSubclassAssigner,
)
from dnd.character.blueprint.building_blocks.subclass_assigner.random import (
    RandomSubclassAssigner,
)
from dnd.character.blueprint.building_blocks.subclass_assigner.subclass_assigner import (
    WizardSubclassAssigner,
)
from dnd.character.blueprint.building_blocks.tool_proficiency_choice_resolver.random import (
    RandomToolProficiencyChoiceResolver,
)
from dnd.character.blueprint.building_blocks.weapon_adder import WeaponAdder
from dnd.character.blueprint.state import Blueprint
from dnd.character.feature.feature import Feature
from dnd.character.feature.feats import FeatName
from dnd.character.race.race import Race
from dnd.character.race.subraces import SubraceName
from dnd.choices.alignment import Alignment
from dnd.choices.background_creatrion.background import Background
from dnd.choices.class_creation.character_class import Class, WizardSubclass
from dnd.choices.equipment_creation.weapons import WeaponName
from dnd.choices.sex import Sex
from dnd.choices.stats_creation.statistic import Statistic


_PRIORITY: StatsPriority = (
    Statistic.STRENGTH,
    Statistic.DEXTERITY,
    Statistic.CONSTITUTION,
    Statistic.INTELLIGENCE,
    Statistic.WISDOM,
    Statistic.CHARISMA,
)


class _MinimalBP:
    """Satisfies BlueprintProtocol (__iter__) but lacks all specific protocol fields."""

    def __iter__(self) -> Iterator[tuple[str, object]]:
        return iter([])


class _RacedBP(Blueprint):
    """Blueprint with race, subrace, speed, and dark_vision_range for LevelUp tests."""

    race: Race = Race.HUMAN
    subrace: SubraceName = SubraceName.HUMAN_STANDARD_HUMAN_PLAYERSHANDBOOK
    speed: int = 30
    dark_vision_range: int = 0


def _exhaust(gen: Generator[object, object, object]) -> object:
    try:
        while True:
            next(gen)
    except StopIteration as exc:
        return exc.value


@pytest.mark.unit
class TestBuildingBlockBase:
    def test_flatten_leaf_block_returns_self(self) -> None:
        b1 = NullBlock()
        assert tuple(b1.flatten()) == (b1,)

    def test_minimal_bp_iter_returns_empty(self) -> None:
        assert list(_MinimalBP()) == []


@pytest.mark.unit
class TestSimpleBlocks:
    def test_age_assigner_get_change(self) -> None:
        block = AgeAssigner(age=30)
        result = _exhaust(block.get_change(Blueprint()))
        assert result is not None

    def test_alignment_assigner_get_change(self) -> None:
        block = AlignmentAssigner(alignment=Alignment.LAWFUL_GOOD)
        result = _exhaust(block.get_change(Blueprint()))
        assert result is not None

    def test_background_assigner_get_change(self) -> None:
        block = BackgroundAssigner(background=Background.SOLDIER)
        result = _exhaust(block.get_change(Blueprint()))
        assert result is not None

    def test_name_assigner_get_change(self) -> None:
        block = NameAssigner(name="Gandalf")
        result = _exhaust(block.get_change(Blueprint()))
        assert result is not None

    def test_sex_assigner_get_change(self) -> None:
        block = SexAssigner(sex=Sex.FEMALE)
        result = _exhaust(block.get_change(Blueprint()))
        assert result is not None

    def test_null_block_get_change(self) -> None:
        block = NullBlock()
        result = _exhaust(block.get_change(Blueprint()))
        assert result is not None

    def test_null_block_apply_returns_same_state(self) -> None:
        block = NullBlock()
        state = Blueprint()
        result = _exhaust(block.get_change(state))
        assert dict(result) == dict(state)


@pytest.mark.unit
class TestEquipmentBlocks:
    def test_weapon_adder_get_change(self) -> None:
        block = WeaponAdder(weapon=WeaponName.DAGGER)
        result = _exhaust(block.get_change(Blueprint()))
        assert result is not None

    def test_equipment_adder_get_change(self) -> None:
        block = EquipmentAdder(item="Rope (50 feet)")
        result = _exhaust(block.get_change(Blueprint()))
        assert result is not None

    def test_feat_adder_get_change(self) -> None:
        block = FeatAdder(feat=FeatName.ALERT)
        result = _exhaust(block.get_change(Blueprint()))
        assert result is not None

    def test_feat_adder_duplicate_feat_raises(self) -> None:
        state_gen = FeatAdder(feat=FeatName.ALERT).get_change(Blueprint())
        try:
            while True:
                next(state_gen)
        except StopIteration as exc:
            state_with_feat = exc.value
        block = FeatAdder(feat=FeatName.ALERT)
        with pytest.raises(ValueError, match="already exists"):
            next(block.get_change(state_with_feat))

    def test_feature_assigner_get_change(self) -> None:
        feature = Feature()
        block = FeatureAssigner(feature=feature)
        result = _exhaust(block.get_change(Blueprint()))
        assert result is not None


@pytest.mark.unit
class TestRandomMagicalItemChooser:
    def test_no_items_returns_empty(self) -> None:
        block = RandomMagicalItemChooser()
        result = _exhaust(block.get_change(Blueprint()))
        assert result is not None

    def test_select_uncommon_item(self) -> None:
        block = RandomMagicalItemChooser(n_uncommon=1, seed=42)
        result = _exhaust(block.get_change(Blueprint()))
        assert result is not None


@pytest.mark.unit
class TestGetChangeTypeErrors:
    def test_weapon_adder_requires_weapons(self) -> None:
        with pytest.raises(TypeError):
            next(WeaponAdder(weapon=WeaponName.DAGGER).get_change(_MinimalBP()))

    def test_equipment_adder_requires_other_equipment(self) -> None:
        with pytest.raises(TypeError):
            next(EquipmentAdder(item="Rope").get_change(_MinimalBP()))

    def test_feat_adder_requires_feats(self) -> None:
        with pytest.raises(TypeError):
            next(FeatAdder(feat=FeatName.ALERT).get_change(_MinimalBP()))

    def test_health_increase_requires_classes(self) -> None:
        with pytest.raises(TypeError):
            next(HealthIncreaseAverage(class_=Class.WIZARD).get_change(_MinimalBP()))

    def test_wizard_level_incrementer_requires_level(self) -> None:
        with pytest.raises(TypeError):
            next(WizardLevelIncrementer().get_change(_MinimalBP()))

    def test_race_assigner_requires_stats(self) -> None:
        with pytest.raises(TypeError):
            next(
                HumanRaceAssigner(
                    subrace=SubraceName.HUMAN_STANDARD_HUMAN_PLAYERSHANDBOOK
                ).get_change(_MinimalBP())
            )

    def test_priority_stat_resolver_requires_stat_protocol(self) -> None:
        with pytest.raises(TypeError):
            next(
                PriorityStatChoiceResolver(priority=_PRIORITY).get_change(_MinimalBP())
            )

    def test_random_skill_resolver_requires_skill_protocol(self) -> None:
        with pytest.raises(TypeError):
            next(RandomSkillChoiceResolver().get_change(_MinimalBP()))

    def test_random_tool_resolver_requires_tool_proficiencies(self) -> None:
        with pytest.raises(TypeError):
            next(RandomToolProficiencyChoiceResolver().get_change(_MinimalBP()))

    def test_random_feat_resolver_requires_feat_stats_protocol(self) -> None:
        with pytest.raises(TypeError):
            next(RandomFeatChoiceResolver().get_change(_MinimalBP()))

    def test_max_first_resolver_requires_feat_stats_cup_protocol(self) -> None:
        with pytest.raises(TypeError):
            next(
                MaxFirstResolver(
                    priority=_PRIORITY, then=RandomFeatChoiceResolver()
                ).get_change(_MinimalBP())
            )

    def test_max_if_not_maxed_resolver_requires_feat_stats_cup_protocol(self) -> None:
        with pytest.raises(TypeError):
            next(MaxIfNotMaxedResolver(priority=_PRIORITY).get_change(_MinimalBP()))

    def test_random_language_resolver_requires_languages(self) -> None:
        with pytest.raises(TypeError):
            next(RandomLanguageChoiceResolver().get_change(_MinimalBP()))

    def test_wizard_spell_assigner_requires_wizard_level(self) -> None:
        with pytest.raises(TypeError):
            next(WizardRandomSpellAssigner().get_change(_MinimalBP()))

    def test_sorcerer_spell_assigner_requires_sorcerer_level(self) -> None:
        with pytest.raises(TypeError):
            next(SorcererRandomSpellAssigner().get_change(_MinimalBP()))

    def test_random_equipment_chooser_requires_equipment_choices(self) -> None:
        with pytest.raises(TypeError):
            next(RandomEquipmentChooser().get_change(_MinimalBP()))

    def test_wizard_subclass_assigner_requires_classes_and_subclasses(self) -> None:
        with pytest.raises(TypeError):
            next(
                WizardSubclassAssigner(subclass=WizardSubclass.ABJURATION).get_change(
                    _MinimalBP()
                )
            )

    def test_random_subclass_assigner_requires_classes_and_subclasses(self) -> None:
        with pytest.raises(TypeError):
            next(RandomSubclassAssigner(class_=Class.WIZARD).get_change(_MinimalBP()))

    def test_optional_subclass_assigner_requires_classes_and_subclasses(self) -> None:
        with pytest.raises(TypeError):
            next(
                OptionalSubclassAssigner(
                    assigner=RandomSubclassAssigner(class_=Class.WIZARD)
                ).get_change(_MinimalBP())
            )


@pytest.mark.unit
class TestCombinedBlockGetChange:
    def test_all_choices_resolver_get_change(self) -> None:
        resolver = AllChoicesResolver.model_construct(
            type=BuildingBlockType.ALL_CHOICES_RESOLVER,
            blocks=(NullBlock(),) * 6,
        )
        result = _exhaust(resolver.get_change(Blueprint()))
        assert result is not None

    def test_initial_builder_get_change(self) -> None:
        builder = InitialBuilder.model_construct(
            type=BuildingBlockType.INITIAL_BUILDER,
            blocks=(NullBlock(),) * 4,
        )
        result = _exhaust(builder.get_change(Blueprint()))
        assert result is not None

    def test_level_up_multiple_get_change(self) -> None:
        level_up_multiple = LevelUpMultiple.model_construct(
            type=BuildingBlockType.LEVEL_UP_MULTIPLE,
            blocks=(NullBlock(),),
        )
        result = _exhaust(level_up_multiple.get_change(Blueprint()))
        assert result is not None

    def test_level_up_get_change(self) -> None:
        level_up = LevelUp.model_construct(
            type=BuildingBlockType.LEVEL_UP,
            blocks=(NullBlock(),) * 4,
        )
        result = _exhaust(level_up.get_change(_RacedBP()))
        assert result is not None
