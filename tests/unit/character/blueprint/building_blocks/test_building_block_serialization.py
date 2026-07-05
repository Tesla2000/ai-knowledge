from __future__ import annotations

import pytest
from dnd.character.blueprint.building_blocks import (
    AnyBuildingBlock,
)
from dnd.character.blueprint.building_blocks import (
    CombinedBlock,
)
from dnd.character.blueprint.building_blocks import (
    ElfRaceAssigner,
)
from dnd.character.blueprint.building_blocks import (
    GnomeRaceAssigner,
)
from dnd.character.blueprint.building_blocks import (
    HalflingRaceAssigner,
)
from dnd.character.blueprint.building_blocks import (
    HumanRaceAssigner,
)
from dnd.character.blueprint.building_blocks import (
    RandomMagicalItemChooser,
)
from dnd.character.blueprint.building_blocks import (
    SexAssigner,
)
from dnd.character.blueprint.building_blocks import (
    TieflingRaceAssigner,
)
from dnd.character.blueprint.building_blocks.building_block import (
    BuildingBlock,
)
from dnd.character.race.subraces import SubraceName
from dnd.choices.sex import Sex
from pydantic import TypeAdapter
from pydantic import ValidationError


@pytest.mark.unit
class TestBuildingBlockSerialization:
    """Test serialization and deserialization of BuildingBlocks."""

    def test_serialize_simple_block(self):
        """Test serializing a simple building block using model_dump."""
        block = SexAssigner(sex=Sex.MALE)
        serialized = block.model_dump()

        assert serialized["block_type"] == "SexAssigner"
        assert serialized["sex"] == Sex.MALE

    def test_deserialize_simple_block(self):
        """Test deserializing a simple building block using model_validate."""
        data = {"block_type": "SexAssigner", "sex": Sex.MALE}
        block = TypeAdapter(AnyBuildingBlock).validate_python(data)

        assert isinstance(block, SexAssigner)
        assert block.sex == Sex.MALE
        assert block.block_type == "SexAssigner"

    def test_roundtrip_simple_block(self):
        """Test serialize-deserialize roundtrip for simple block."""
        original = SexAssigner(sex=Sex.FEMALE)
        serialized = original.model_dump()

        deserialized = TypeAdapter(AnyBuildingBlock).validate_python(serialized)

        assert isinstance(deserialized, SexAssigner)
        assert deserialized.sex == original.sex
        assert deserialized == original

    def test_serialize_complex_block(self):
        """Test serializing a more complex building block."""
        block = ElfRaceAssigner(subrace=SubraceName.ELF_HIGH_ELF_PLAYERSHANDBOOK)
        serialized = block.model_dump()

        assert serialized["block_type"] == "ElfRaceAssigner"
        assert serialized["subrace"] == SubraceName.ELF_HIGH_ELF_PLAYERSHANDBOOK

    def test_roundtrip_complex_block(self):
        """Test serialize-deserialize roundtrip for complex block."""
        original = HalflingRaceAssigner(
            subrace=SubraceName.HALFLING_LIGHTFOOT_PLAYERSHANDBOOK
        )
        serialized = original.model_dump()

        deserialized = TypeAdapter(AnyBuildingBlock).validate_python(serialized)

        assert isinstance(deserialized, HalflingRaceAssigner)
        assert deserialized.subrace == original.subrace
        assert deserialized == original

    def test_serialize_combined_block(self):
        """Test serializing a CombinedBlock containing multiple blocks."""
        block1 = SexAssigner(sex=Sex.MALE)
        block2 = HumanRaceAssigner(
            subrace=SubraceName.HUMAN_STANDARD_HUMAN_PLAYERSHANDBOOK
        )
        combined = CombinedBlock(blocks=(block1, block2))

        serialized = combined.model_dump()

        assert serialized["block_type"] == "CombinedBlock"
        assert len(serialized["blocks"]) == 2
        assert serialized["blocks"][0]["block_type"] == "SexAssigner"
        assert serialized["blocks"][1]["block_type"] == "HumanRaceAssigner"

    def test_serialize_and_deserialize_base_block_json(self, building_blocks):
        """Test serializing a CombinedBlock containing multiple blocks."""
        serialized = building_blocks.model_dump(mode="json")
        assert (
            TypeAdapter(AnyBuildingBlock).validate_python(serialized) == building_blocks
        )

    def test_deserialize_combined_block(self):
        """Test deserializing a CombinedBlock."""
        data = {
            "block_type": "CombinedBlock",
            "blocks": [
                {"block_type": "SexAssigner", "sex": Sex.FEMALE},
                {
                    "block_type": "ElfRaceAssigner",
                    "subrace": SubraceName.ELF_WOOD_ELF_PLAYERSHANDBOOK,
                },
            ],
        }

        block = TypeAdapter(AnyBuildingBlock).validate_python(data)

        assert isinstance(block, CombinedBlock)
        assert len(block.blocks) == 2
        assert isinstance(block.blocks[0], SexAssigner)
        assert isinstance(block.blocks[1], ElfRaceAssigner)
        assert block.blocks[0].sex == Sex.FEMALE
        assert block.blocks[1].subrace == SubraceName.ELF_WOOD_ELF_PLAYERSHANDBOOK

    def test_roundtrip_combined_block(self):
        """Test serialize-deserialize roundtrip for CombinedBlock."""
        block1 = SexAssigner(sex=Sex.MALE)
        block2 = TieflingRaceAssigner(
            subrace=SubraceName.TIEFLING_BLOODLINE_OF_ASMODEUS_PLAYERSHANDBOOK
        )
        original = CombinedBlock(blocks=(block1, block2))

        serialized = original.model_dump()

        deserialized = TypeAdapter(AnyBuildingBlock).validate_python(serialized)

        assert isinstance(deserialized, CombinedBlock)
        assert len(deserialized.blocks) == 2
        assert deserialized.blocks[0] == block1
        assert deserialized.blocks[1] == block2
        assert deserialized == original

    def test_grandchild_block(self):
        """Test serialize-deserialize roundtrip for CombinedBlock."""
        block = RandomMagicalItemChooser()
        assert BuildingBlock not in type(block).__bases__ and isinstance(
            block, BuildingBlock
        )
        serialized = block.model_dump()
        deserialized = TypeAdapter(AnyBuildingBlock).validate_python(serialized)
        assert deserialized == block

    def test_roundtrip_incomplete_data(self):
        """Test serialize-deserialize roundtrip for CombinedBlock."""
        block1 = SexAssigner(sex=Sex.MALE)
        block2 = TieflingRaceAssigner(
            subrace=SubraceName.TIEFLING_BLOODLINE_OF_ASMODEUS_PLAYERSHANDBOOK
        )
        original = CombinedBlock(blocks=(block1, block2))

        serialized = original.model_dump()
        serialized["blocks"][0].pop("sex")
        with pytest.raises(ValidationError):
            TypeAdapter(AnyBuildingBlock).validate_python(serialized)

    def test_block_type_auto_set(self):
        """Test that block_type is automatically set on creation."""
        block = SexAssigner(sex=Sex.MALE)
        assert block.block_type == "SexAssigner"

        race_block = GnomeRaceAssigner(
            subrace=SubraceName.GNOME_FOREST_GNOME_PLAYERSHANDBOOK
        )
        assert race_block.block_type == "GnomeRaceAssigner"

    def test_combined_block_with_nested_combined(self):
        """Test CombinedBlock can contain other CombinedBlocks."""
        block1 = SexAssigner(sex=Sex.MALE)
        block2 = HumanRaceAssigner(
            subrace=SubraceName.HUMAN_STANDARD_HUMAN_PLAYERSHANDBOOK
        )
        inner_combined = CombinedBlock(blocks=(block1, block2))

        block3 = SexAssigner(sex=Sex.FEMALE)
        outer_combined = CombinedBlock(blocks=(inner_combined, block3))

        serialized = outer_combined.model_dump()
        deserialized = TypeAdapter(AnyBuildingBlock).validate_python(serialized)

        assert isinstance(deserialized, CombinedBlock)
        assert len(deserialized.blocks) == 2
        assert isinstance(deserialized.blocks[0], CombinedBlock)
        assert isinstance(deserialized.blocks[1], SexAssigner)
        assert deserialized == outer_combined
