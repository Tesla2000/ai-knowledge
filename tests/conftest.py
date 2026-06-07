import pytest
from dnd.character.builder import Builder
from dnd.character.checkpoint import IncrementStorage
from dnd.character.checkpoint import MemoryStorage
from dnd.server.example_generators.example_building_blocks import (
    example_building_blocks,
)


@pytest.fixture()
def increment_storage() -> IncrementStorage:
    return MemoryStorage()


@pytest.fixture
def building_blocks():
    return example_building_blocks()


@pytest.fixture
def base_builder(building_blocks, increment_storage):
    return Builder(
        building_blocks=(building_blocks,), increment_storage=increment_storage
    )
