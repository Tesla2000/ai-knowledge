from __future__ import annotations

from collections.abc import Generator
from typing import cast
from typing import TYPE_CHECKING

from typing_protocol_intersection import ProtocolIntersection

from dnd.character.blueprint.building_blocks.building_block import BuildingBlock
from dnd.character.blueprint.state import Blueprint
from dnd.character.blueprint.state import BlueprintProtocol
from dnd.character.blueprint.state import HasAlignment
from dnd.character.delta.delta import Delta
from dnd.choices.alignment import Alignment
from pydantic import Field


class AlignmentDelta(Delta):
    """Delta produced when AlignmentAssigner sets the character alignment."""

    alignment: Alignment

    def apply[T: BlueprintProtocol](
        self, state: T
    ) -> ProtocolIntersection[T, HasAlignment]:

        if TYPE_CHECKING:

            class BlueprintWithAlignment(Blueprint):
                alignment: Alignment

        else:

            class BlueprintWithAlignment(type(state)):
                alignment: Alignment

        return cast(
            ProtocolIntersection[T, HasAlignment],
            BlueprintWithAlignment.model_validate(
                {**dict(state), "alignment": self.alignment}
            ),
        )


class AlignmentAssigner[T: BlueprintProtocol](
    BuildingBlock[T, AlignmentDelta, HasAlignment]
):
    """Assigns an alignment to the character."""

    alignment: Alignment = Field(description="Character's moral and ethical alignment")

    def get_change(
        self, state: T
    ) -> Generator[AlignmentDelta, None, ProtocolIntersection[T, HasAlignment]]:
        delta = AlignmentDelta(alignment=self.alignment)
        yield delta
        return delta.apply(state)
