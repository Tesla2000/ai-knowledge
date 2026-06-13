from unittest.mock import patch

import pytest
from dnd_character_creator.character.blueprint.blueprint import Blueprint
from dnd_character_creator.character.blueprint.building_blocks import (
    SexAssigner,
)
from dnd_character_creator.character.blueprint.building_blocks.building_block import (
    BuildingBlock,
)
from dnd_character_creator.character.checkpoint import IncrementChain
from dnd_character_creator.character.checkpoint import IncrementStorage
from dnd_character_creator.character.checkpoint import MemoryStorage
from dnd_character_creator.character.presentable_character import (
    PresentableCharacter,
)
from dnd_character_creator.choices.sex import Sex


class TestRestartFromCheckpoint:
    @pytest.fixture
    def increment_storage(self) -> IncrementStorage:
        return MemoryStorage()

    def test_restart_from_checkpoint(self, base_builder, increment_storage):
        result = base_builder.build()
        increment_chain = increment_storage.load_chain(result.chain_id)
        n_truncated_moves = 10
        truncated_chain = increment_chain.truncate_to(
            increment_chain.length() - n_truncated_moves
        )
        with patch.object(
            IncrementChain,
            IncrementChain.add_increment.__name__,
            wraps=IncrementChain.add_increment,
            autospec=True,
        ) as mock_add_increment:
            result = base_builder.build(truncated_chain)
            assert isinstance(result.character, PresentableCharacter)
            assert mock_add_increment.call_count == n_truncated_moves

    def test_checkpoint_on_error(self, base_builder, increment_storage):
        error_message = "Error message"

        class ErrorBuildingBlock(BuildingBlock):
            """Docstring"""

            def get_change(self, blueprint: Blueprint) -> Blueprint:
                raise ValueError(error_message)

        invalid_builder = base_builder.add(ErrorBuildingBlock())
        result = invalid_builder.build()
        assert result.error.args[0] == error_message
        increment_chain = increment_storage.load_chain(result.chain_id)
        n_truncated_moves = 1
        truncated_chain = increment_chain.truncate_to(increment_chain.length())
        valid_builder = base_builder.add(SexAssigner(sex=Sex.MALE))
        with patch.object(
            IncrementChain,
            IncrementChain.add_increment.__name__,
            wraps=IncrementChain.add_increment,
            autospec=True,
        ) as mock_add_increment:
            result = valid_builder.build(truncated_chain)
            assert isinstance(result.character, PresentableCharacter)
            assert mock_add_increment.call_count == n_truncated_moves
