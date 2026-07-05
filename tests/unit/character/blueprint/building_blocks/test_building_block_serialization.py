from __future__ import annotations

import pytest
from dnd.character.blueprint.building_blocks import (
    AnyBuildingBlock,
)
from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
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

        assert serialized["type"] == BuildingBlockType.SEX_ASSIGNER
        assert serialized["sex"] == Sex.MALE

    def test_deserialize_simple_block(self):
        """Test deserializing a simple building block using model_validate."""
        data = {"type": BuildingBlockType.SEX_ASSIGNER, "sex": Sex.MALE}
        block = TypeAdapter(AnyBuildingBlock).validate_python(data)

        assert isinstance(block, SexAssigner)
        assert block.sex == Sex.MALE
        assert block.type == BuildingBlockType.SEX_ASSIGNER

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

        assert serialized["type"] == BuildingBlockType.ELF_RACE_ASSIGNER
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

    def test_serialize_block_sequence(self):
        """Test serializing a sequence containing multiple blocks."""
        block1 = SexAssigner(sex=Sex.MALE)
        block2 = HumanRaceAssigner(
            subrace=SubraceName.HUMAN_STANDARD_HUMAN_PLAYERSHANDBOOK
        )

        serialized = TypeAdapter(tuple[AnyBuildingBlock, ...]).dump_python(
            (block1, block2)
        )

        assert len(serialized) == 2
        assert serialized[0]["type"] == BuildingBlockType.SEX_ASSIGNER
        assert serialized[1]["type"] == BuildingBlockType.HUMAN_RACE_ASSIGNER

    def test_serialize_and_deserialize_base_block_json(self, building_blocks):
        """Test serializing a sequence containing multiple blocks."""
        adapter = TypeAdapter(tuple[AnyBuildingBlock, ...])
        serialized = adapter.dump_python(building_blocks, mode="json")
        assert adapter.validate_python(serialized) == building_blocks

    def test_deserialize_block_sequence(self):
        """Test deserializing a sequence of blocks."""
        data = [
            {"type": BuildingBlockType.SEX_ASSIGNER, "sex": Sex.FEMALE},
            {
                "type": BuildingBlockType.ELF_RACE_ASSIGNER,
                "subrace": SubraceName.ELF_WOOD_ELF_PLAYERSHANDBOOK,
            },
        ]

        blocks = TypeAdapter(tuple[AnyBuildingBlock, ...]).validate_python(data)

        assert len(blocks) == 2
        assert isinstance(blocks[0], SexAssigner)
        assert isinstance(blocks[1], ElfRaceAssigner)
        assert blocks[0].sex == Sex.FEMALE
        assert blocks[1].subrace == SubraceName.ELF_WOOD_ELF_PLAYERSHANDBOOK

    def test_roundtrip_block_sequence(self):
        """Test serialize-deserialize roundtrip for a block sequence."""
        block1 = SexAssigner(sex=Sex.MALE)
        block2 = TieflingRaceAssigner(
            subrace=SubraceName.TIEFLING_BLOODLINE_OF_ASMODEUS_PLAYERSHANDBOOK
        )
        original = (block1, block2)

        adapter = TypeAdapter(tuple[AnyBuildingBlock, ...])
        serialized = adapter.dump_python(original)

        deserialized = adapter.validate_python(serialized)

        assert len(deserialized) == 2
        assert deserialized[0] == block1
        assert deserialized[1] == block2
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
        """Test validation fails when required block data is missing."""
        block1 = SexAssigner(sex=Sex.MALE)
        block2 = TieflingRaceAssigner(
            subrace=SubraceName.TIEFLING_BLOODLINE_OF_ASMODEUS_PLAYERSHANDBOOK
        )
        original = (block1, block2)

        serialized = TypeAdapter(tuple[AnyBuildingBlock, ...]).dump_python(original)
        serialized[0].pop("sex")
        with pytest.raises(ValidationError):
            TypeAdapter(tuple[AnyBuildingBlock, ...]).validate_python(serialized)

    def test_block_type_auto_set(self):
        """Test that block_type is automatically set on creation."""
        block = SexAssigner(sex=Sex.MALE)
        assert block.type == BuildingBlockType.SEX_ASSIGNER

        race_block = GnomeRaceAssigner(
            subrace=SubraceName.GNOME_FOREST_GNOME_PLAYERSHANDBOOK
        )
        assert race_block.type == BuildingBlockType.GNOME_RACE_ASSIGNER
