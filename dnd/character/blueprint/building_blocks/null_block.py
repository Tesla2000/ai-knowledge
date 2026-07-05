from __future__ import annotations

from collections.abc import Generator

from typing_protocol_intersection import ProtocolIntersection

from dnd.character.blueprint.building_blocks.building_block import BuildingBlock
from dnd.character.blueprint.state import BlueprintProtocol
from dnd.character.delta.delta import Delta
from typing import Literal
from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)


class NullDelta(Delta):
    """Delta that applies no changes."""

    delta_type: Literal["NullDelta"] = "NullDelta"

    def apply[T: BlueprintProtocol](
        self, state: T
    ) -> ProtocolIntersection[T, BlueprintProtocol]:
        return state


class NullBlock(BuildingBlock):
    """A building block that applies no changes to the blueprint.

    Useful as a placeholder or default no-op building block when
    a block is required but no modification is needed.
    """

    type: Literal[BuildingBlockType.NULL_BLOCK] = BuildingBlockType.NULL_BLOCK

    def get_change[T: BlueprintProtocol](
        self, state: T
    ) -> Generator[NullDelta, None, ProtocolIntersection[T, BlueprintProtocol]]:
        delta = NullDelta()
        yield delta
        return delta.apply(state)
