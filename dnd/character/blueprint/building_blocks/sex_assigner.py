from __future__ import annotations

from collections.abc import Generator
from typing import cast
from typing import Literal
from typing import TYPE_CHECKING

from typing_protocol_intersection import ProtocolIntersection

from dnd.character.blueprint.building_blocks.building_block import BuildingBlock
from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)
from dnd.character.blueprint.state import Blueprint
from dnd.character.blueprint.state import BlueprintProtocol
from dnd.character.blueprint.state import HasSex
from dnd.character.delta.delta import Delta
from dnd.choices.sex import Sex
from pydantic import Field


class SexDelta(Delta):
    """Delta produced when SexAssigner sets the character sex."""

    delta_type: Literal["SexDelta"] = "SexDelta"
    sex: Sex

    def apply[T: BlueprintProtocol](self, state: T) -> ProtocolIntersection[T, HasSex]:

        if TYPE_CHECKING:

            class BlueprintWithSex(Blueprint):
                sex: Sex

        else:

            class BlueprintWithSex(type(state)):
                sex: Sex

        return cast(
            ProtocolIntersection[T, HasSex],
            BlueprintWithSex.model_validate({**dict(state), "sex": self.sex}),
        )


class SexAssigner(BuildingBlock):
    """Assigns a sex to the character."""

    type: Literal[BuildingBlockType.SEX_ASSIGNER] = BuildingBlockType.SEX_ASSIGNER
    sex: Sex = Field(description="Character's biological sex")

    def get_change[T: BlueprintProtocol](
        self, state: T
    ) -> Generator[SexDelta, None, ProtocolIntersection[T, HasSex]]:
        delta = SexDelta(sex=self.sex)
        yield delta
        return delta.apply(state)
