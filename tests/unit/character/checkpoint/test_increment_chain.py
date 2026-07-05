from __future__ import annotations

import pytest

from dnd.character.blueprint.building_blocks.null_block import NullBlock
from dnd.character.blueprint.state import Blueprint
from dnd.character.checkpoint.increment_chain import IncrementChain


@pytest.mark.unit
class TestIncrementChain:
    def test_truncate_to_negative_raises(self) -> None:
        chain = IncrementChain()
        with pytest.raises(IndexError):
            chain.truncate_to(-1)

    def test_truncate_to_above_length_raises(self) -> None:
        chain = IncrementChain()
        with pytest.raises(IndexError):
            chain.truncate_to(1)

    def test_len_empty_chain(self) -> None:
        chain = IncrementChain()
        assert len(chain) == 0

    def test_len_after_increments(self) -> None:
        block = NullBlock()
        gen = block.get_change(Blueprint())
        try:
            delta = next(gen)
        except StopIteration:
            return
        chain = IncrementChain().add_increment(delta)
        assert len(chain) == 1

    def test_truncate_to_zero_returns_empty(self) -> None:
        block = NullBlock()
        gen = block.get_change(Blueprint())
        try:
            delta = next(gen)
        except StopIteration:
            return
        chain = IncrementChain().add_increment(delta)
        truncated = chain.truncate_to(0)
        assert len(truncated) == 0
