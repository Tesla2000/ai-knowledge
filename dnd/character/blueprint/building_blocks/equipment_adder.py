from __future__ import annotations

from collections.abc import Generator
from typing import cast
from typing import TYPE_CHECKING

from typing_protocol_intersection import ProtocolIntersection

from dnd.character.blueprint.building_blocks.building_block import BuildingBlock
from dnd.character.blueprint.state import Blueprint
from dnd.character.blueprint.state import BlueprintProtocol
from dnd.character.blueprint.state import HasOtherEquipment
from dnd.character.delta.delta import Delta
from pydantic import Field


class OtherEquipmentDelta(Delta):
    """Delta produced when EquipmentAdder appends an item."""

    other_equipment: tuple[str, ...]

    def apply[T: BlueprintProtocol](
        self, state: T
    ) -> ProtocolIntersection[T, HasOtherEquipment]:

        if TYPE_CHECKING:

            class BlueprintWithOtherEquipment(Blueprint):
                other_equipment: tuple[str, ...]

        else:

            class BlueprintWithOtherEquipment(type(state)):
                other_equipment: tuple[str, ...]

        return cast(
            ProtocolIntersection[T, HasOtherEquipment],
            BlueprintWithOtherEquipment.model_validate(
                {**dict(state), "other_equipment": self.other_equipment}
            ),
        )


class EquipmentAdder[T: HasOtherEquipment](
    BuildingBlock[T, OtherEquipmentDelta, HasOtherEquipment]
):
    """Adds an item to the character's other equipment list."""

    item: str = Field(description="Equipment item to add to character's inventory")

    def get_change(
        self, state: T
    ) -> Generator[
        OtherEquipmentDelta, None, ProtocolIntersection[T, HasOtherEquipment]
    ]:
        delta = OtherEquipmentDelta(
            other_equipment=state.other_equipment + (self.item,)
        )
        yield delta
        return delta.apply(state)
