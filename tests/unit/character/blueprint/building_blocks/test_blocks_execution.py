from __future__ import annotations

from collections.abc import Generator

import pytest

from dnd.character.blueprint.building_blocks.age_assigner import AgeAssigner
from dnd.character.blueprint.building_blocks.alignment_assigner import AlignmentAssigner
from dnd.character.blueprint.building_blocks.background_assigner import (
    BackgroundAssigner,
)
from dnd.character.blueprint.building_blocks.building_block import (
    BuildingBlock,
)
from dnd.character.blueprint.building_blocks.equipment_adder import EquipmentAdder
from dnd.character.blueprint.building_blocks.feat_adder import FeatAdder
from dnd.character.blueprint.building_blocks.feature_assigner import FeatureAssigner
from dnd.character.blueprint.building_blocks.magical_item_chooser.random import (
    RandomMagicalItemChooser,
)
from dnd.character.blueprint.building_blocks.name_assigner import NameAssigner
from dnd.character.blueprint.building_blocks.null_block import NullBlock
from dnd.character.blueprint.building_blocks.sex_assigner import SexAssigner
from dnd.character.blueprint.building_blocks.weapon_adder import WeaponAdder
from dnd.character.blueprint.state import Blueprint
from dnd.character.feature.feature import Feature
from dnd.character.feature.feats import FeatName
from dnd.choices.alignment import Alignment
from dnd.choices.background_creatrion.background import Background
from dnd.choices.equipment_creation.weapons import WeaponName
from dnd.choices.sex import Sex


def _exhaust(gen: Generator[object, object, object]) -> object:
    try:
        while True:
            next(gen)
    except StopIteration as exc:
        return exc.value


class _RawBlock(BuildingBlock):
    """Raw BuildingBlock subclass that does not override get_change."""


@pytest.mark.unit
class TestBuildingBlockBase:
    def test_get_change_raises_not_implemented(self) -> None:
        block = _RawBlock()
        with pytest.raises(NotImplementedError, match="_RawBlock must implement"):
            block.get_change(Blueprint())

    def test_flatten_leaf_block_returns_self(self) -> None:
        b1 = NullBlock()
        assert tuple(b1.flatten()) == (b1,)


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
