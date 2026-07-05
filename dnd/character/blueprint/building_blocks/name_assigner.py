from __future__ import annotations

from collections.abc import Generator
from typing import Literal
from typing import cast
from typing import TYPE_CHECKING

from typing_protocol_intersection import ProtocolIntersection

from dnd.character.blueprint.building_blocks.building_block import BuildingBlock
from dnd.character.blueprint.state import Blueprint
from dnd.character.blueprint.state import BlueprintProtocol
from dnd.character.blueprint.state import HasName
from dnd.character.delta.delta import Delta
from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)
from pydantic import Field


class NameDelta(Delta):
    """Delta produced when NameAssigner sets the character name."""

    delta_type: Literal["NameDelta"] = "NameDelta"
    name: str

    def apply[T: BlueprintProtocol](self, state: T) -> ProtocolIntersection[T, HasName]:

        if TYPE_CHECKING:

            class BlueprintWithName(Blueprint):
                name: str

        else:

            class BlueprintWithName(type(state)):
                name: str

        return cast(
            ProtocolIntersection[T, HasName],
            BlueprintWithName.model_validate({**dict(state), "name": self.name}),
        )


class NameAssigner(BuildingBlock):
    """Assigns a name to the character."""

    type: Literal[BuildingBlockType.NAME_ASSIGNER] = BuildingBlockType.NAME_ASSIGNER

    name: str = Field(description="Character's full name")

    def get_change[T: BlueprintProtocol](
        self, state: T
    ) -> Generator[NameDelta, None, ProtocolIntersection[T, HasName]]:
        delta = NameDelta(name=self.name)
        yield delta
        return delta.apply(state)
