import pytest

from dnd.character.blueprint.building_blocks.all_choices_resolver.base import (
    AllChoicesResolver,
)
from dnd.character.blueprint.building_blocks.initial_data_filler.random_filler import (
    RandomInitialDataFiller,
)
from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)
from dnd.character.blueprint.building_blocks.equipment_adder import EquipmentAdder
from dnd.character.blueprint.building_blocks.feat_adder import FeatAdder
from dnd.character.blueprint.building_blocks.feature_assigner import FeatureAssigner
from dnd.character.blueprint.building_blocks.initial_builder import InitialBuilder
from dnd.character.blueprint.building_blocks.magical_item_chooser.random import (
    RandomMagicalItemChooser,
)
from dnd.character.blueprint.building_blocks.null_block import NullBlock
from dnd.character.blueprint.building_blocks.stats_priority import StatsPriority
from dnd.character.blueprint.building_blocks.weapon_adder import WeaponAdder
from dnd.character.blueprint.states.state import Blueprint
from dnd.character.feature.feature import Feature
from dnd.character.feature.feats import FeatName
from dnd.choices.equipment_creation.weapons import WeaponName
from dnd.choices.stats_creation.statistic import Statistic


_PRIORITY: StatsPriority = (
    Statistic.STRENGTH,
    Statistic.DEXTERITY,
    Statistic.CONSTITUTION,
    Statistic.INTELLIGENCE,
    Statistic.WISDOM,
    Statistic.CHARISMA,
)


@pytest.mark.unit
class TestSimpleBlocks:
    def test_random_initial_data_filler_apply(self) -> None:
        block = RandomInitialDataFiller(seed=42)
        result = block.apply(Blueprint())
        assert result.character_data is not None
        assert result.character_data.name is not None
        assert result.character_data.sex is not None

    def test_null_block_apply(self) -> None:
        block = NullBlock()
        result = block.apply(Blueprint())
        assert result is not None

    def test_null_block_apply_returns_same_state(self) -> None:
        block = NullBlock()
        state = Blueprint()
        result = block.apply(state)
        assert dict(result) == dict(state)


@pytest.mark.unit
class TestEquipmentBlocks:
    def test_weapon_adder_apply(self) -> None:
        block = WeaponAdder(weapon=WeaponName.DAGGER)
        result = block.apply(Blueprint())
        assert result is not None

    def test_equipment_adder_apply(self) -> None:
        block = EquipmentAdder(item="Rope (50 feet)")
        result = block.apply(Blueprint())
        assert result is not None

    def test_feat_adder_apply(self) -> None:
        block = FeatAdder(feat=FeatName.ALERT)
        result = block.apply(Blueprint())
        assert result is not None

    def test_feat_adder_duplicate_feat_raises(self) -> None:
        state_with_feat = FeatAdder(feat=FeatName.ALERT).apply(Blueprint())
        block = FeatAdder(feat=FeatName.ALERT)
        with pytest.raises(ValueError, match="already exists"):
            block.apply(state_with_feat)

    def test_feature_assigner_apply(self) -> None:
        feature = Feature()
        block = FeatureAssigner(feature=feature)
        result = block.apply(Blueprint())
        assert result is not None


@pytest.mark.unit
class TestRandomMagicalItemChooser:
    def test_no_items_returns_empty(self) -> None:
        block = RandomMagicalItemChooser()
        result = block.apply(Blueprint())
        assert result is not None

    def test_select_uncommon_item(self) -> None:
        block = RandomMagicalItemChooser(n_uncommon=1, seed=42)
        result = block.apply(Blueprint())
        assert result is not None


@pytest.mark.unit
class TestCombinedBlockApply:
    def test_all_choices_resolver_apply(self) -> None:
        resolver = AllChoicesResolver.model_construct(
            type=BuildingBlockType.ALL_CHOICES_RESOLVER,
            language_choice_resolver=NullBlock(),
            skill_choice_resolver=NullBlock(),
            feat_choice_resolver=NullBlock(),
            tool_proficiency_choice_resolver=NullBlock(),
            stat_choice_resolver=NullBlock(),
            equipment_chooser=NullBlock(),
        )
        result = resolver.apply(Blueprint())
        assert result is not None

    def test_initial_builder_apply(self) -> None:
        builder = InitialBuilder.model_construct(
            type=BuildingBlockType.INITIAL_BUILDER,
            level_assigner=NullBlock(),
            stats_builder=NullBlock(),
            race_assigner=NullBlock(),
            all_choices_resolver=NullBlock(),
        )
        result = builder.apply(Blueprint())
        assert result is not None
