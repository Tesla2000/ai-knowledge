from __future__ import annotations

from collections.abc import Generator
from typing import cast
from typing import TYPE_CHECKING

from typing_protocol_intersection import ProtocolIntersection

from dnd.character.blueprint.building_blocks.building_block import BuildingBlock
from dnd.character.blueprint.state import Blueprint
from dnd.character.blueprint.state import BlueprintProtocol
from dnd.character.blueprint.state import HasLevel
from dnd.character.character import ClassLevel
from pydantic import Field
from dnd.character.delta.delta import Delta


class LevelDelta(Delta):
    """Delta produced when LevelAssigner sets the character level."""

    level: ClassLevel

    def apply[T: BlueprintProtocol](
        self, state: T
    ) -> ProtocolIntersection[T, HasLevel]:

        if TYPE_CHECKING:

            class BlueprintWithLevel(Blueprint):
                level: ClassLevel

        else:

            class BlueprintWithLevel(type(state)):
                level: ClassLevel

        return cast(
            ProtocolIntersection[T, HasLevel],
            BlueprintWithLevel.model_validate({**dict(state), "level": self.level}),
        )


class LevelAssigner[T: BlueprintProtocol](BuildingBlock[T, LevelDelta, HasLevel]):
    """Assigns a level to the character."""

    level: ClassLevel = Field(description="The character's total level (1–20)")

    def get_change(
        self, state: T
    ) -> Generator[LevelDelta, None, ProtocolIntersection[T, HasLevel]]:
        delta = LevelDelta(level=self.level)
        yield delta
        return delta.apply(state)
