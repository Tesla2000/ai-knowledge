from __future__ import annotations

from collections.abc import Generator

from typing_protocol_intersection import ProtocolIntersection

from dnd.character.blueprint.building_blocks.building_block import BuildingBlock
from dnd.character.blueprint.state import BlueprintProtocol
from dnd.character.delta.delta import Delta


class NullDelta(Delta):
    """Delta that applies no changes."""

    def apply[T: BlueprintProtocol](
        self, state: T
    ) -> ProtocolIntersection[T, BlueprintProtocol]:
        return state


class NullBlock[T: BlueprintProtocol](BuildingBlock[T, NullDelta, BlueprintProtocol]):
    """A building block that applies no changes to the blueprint.

    Useful as a placeholder or default no-op building block when
    a block is required but no modification is needed.
    """

    def get_change(
        self, state: T
    ) -> Generator[NullDelta, None, ProtocolIntersection[T, BlueprintProtocol]]:
        delta = NullDelta()
        yield delta
        return delta.apply(state)
