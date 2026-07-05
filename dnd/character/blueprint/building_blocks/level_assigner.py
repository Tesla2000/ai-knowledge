from __future__ import annotations

from collections.abc import Generator
from typing import Literal
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
from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)


class LevelDelta(Delta):
    """Delta produced when LevelAssigner sets the character level."""

    delta_type: Literal["LevelDelta"] = "LevelDelta"
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


class LevelAssigner(BuildingBlock):
    """Assigns a level to the character."""

    type: Literal[BuildingBlockType.LEVEL_ASSIGNER] = BuildingBlockType.LEVEL_ASSIGNER

    level: ClassLevel = Field(description="The character's total level (1–20)")

    def get_change[T: BlueprintProtocol](
        self, state: T
    ) -> Generator[LevelDelta, None, ProtocolIntersection[T, HasLevel]]:
        delta = LevelDelta(level=self.level)
        yield delta
        return delta.apply(state)
