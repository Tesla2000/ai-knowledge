from __future__ import annotations

from collections.abc import Generator
from typing import Literal
from typing import cast
from typing import TYPE_CHECKING

from typing_protocol_intersection import ProtocolIntersection

from dnd.character.blueprint.building_blocks.building_block import BuildingBlock
from dnd.character.blueprint.state import Blueprint
from dnd.character.blueprint.state import BlueprintProtocol
from dnd.character.blueprint.state import HasAge
from dnd.character.delta.delta import Delta
from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)
from pydantic import Field
from pydantic import PositiveInt


class AgeDelta(Delta):
    """Delta produced when AgeAssigner sets the character age."""

    delta_type: Literal["AgeDelta"] = "AgeDelta"
    age: PositiveInt

    def apply[T: BlueprintProtocol](self, state: T) -> ProtocolIntersection[T, HasAge]:

        if TYPE_CHECKING:

            class BlueprintWithAge(Blueprint):
                age: PositiveInt

        else:

            class BlueprintWithAge(type(state)):
                age: PositiveInt

        return cast(
            ProtocolIntersection[T, HasAge],
            BlueprintWithAge.model_validate({**dict(state), "age": self.age}),
        )


class AgeAssigner(BuildingBlock):
    """Assigns an age to the character."""

    type: Literal[BuildingBlockType.AGE_ASSIGNER] = BuildingBlockType.AGE_ASSIGNER

    age: PositiveInt = Field(description="Character's age in years")

    def get_change[T: BlueprintProtocol](
        self, state: T
    ) -> Generator[AgeDelta, None, ProtocolIntersection[T, HasAge]]:
        delta = AgeDelta(age=self.age)
        yield delta
        return delta.apply(state)
