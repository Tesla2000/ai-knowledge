from __future__ import annotations

from collections.abc import Generator
from typing import cast
from typing import TYPE_CHECKING

from typing_protocol_intersection import ProtocolIntersection

from dnd.character.blueprint.building_blocks.building_block import BuildingBlock
from dnd.character.blueprint.state import Blueprint
from dnd.character.blueprint.state import BlueprintProtocol
from dnd.character.blueprint.state import HasAge
from dnd.character.delta.delta import Delta
from pydantic import Field
from pydantic import PositiveInt


class AgeDelta(Delta):
    """Delta produced when AgeAssigner sets the character age."""

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


class AgeAssigner[T: BlueprintProtocol](BuildingBlock[T, AgeDelta, HasAge]):
    """Assigns an age to the character."""

    age: PositiveInt = Field(description="Character's age in years")

    def get_change(
        self, state: T
    ) -> Generator[AgeDelta, None, ProtocolIntersection[T, HasAge]]:
        delta = AgeDelta(age=self.age)
        yield delta
        return delta.apply(state)
