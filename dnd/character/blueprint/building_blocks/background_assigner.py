from __future__ import annotations

from collections.abc import Generator
from typing import Literal
from typing import cast
from typing import TYPE_CHECKING

from typing_protocol_intersection import ProtocolIntersection

from dnd.character.blueprint.building_blocks.building_block import BuildingBlock
from dnd.character.blueprint.state import Blueprint
from dnd.character.blueprint.state import BlueprintProtocol
from dnd.character.blueprint.state import HasBackground
from dnd.character.delta.delta import Delta
from dnd.choices.background_creatrion.background import Background
from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)
from pydantic import Field


class BackgroundDelta(Delta):
    """Delta produced when BackgroundAssigner sets the character background."""

    delta_type: Literal["BackgroundDelta"] = "BackgroundDelta"
    background: Background

    def apply[T: BlueprintProtocol](
        self, state: T
    ) -> ProtocolIntersection[T, HasBackground]:

        if TYPE_CHECKING:

            class BlueprintWithBackground(Blueprint):
                background: Background

        else:

            class BlueprintWithBackground(type(state)):
                background: Background

        return cast(
            ProtocolIntersection[T, HasBackground],
            BlueprintWithBackground.model_validate(
                {**dict(state), "background": self.background}
            ),
        )


class BackgroundAssigner(BuildingBlock):
    """Assigns a background to the character."""

    type: Literal[BuildingBlockType.BACKGROUND_ASSIGNER] = (
        BuildingBlockType.BACKGROUND_ASSIGNER
    )

    background: Background = Field(
        description="Character's background story and origin"
    )

    def get_change[T: BlueprintProtocol](
        self, state: T
    ) -> Generator[BackgroundDelta, None, ProtocolIntersection[T, HasBackground]]:
        delta = BackgroundDelta(background=self.background)
        yield delta
        return delta.apply(state)
