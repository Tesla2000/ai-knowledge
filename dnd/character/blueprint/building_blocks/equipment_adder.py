from __future__ import annotations

from collections.abc import Generator
from typing import Literal
from typing import cast
from typing import overload
from typing import TYPE_CHECKING

from typing_extensions import deprecated
from typing_protocol_intersection import ProtocolIntersection

from dnd.character.blueprint.building_blocks.building_block import BuildingBlock
from dnd.character.blueprint.state import Blueprint
from dnd.character.blueprint.state import BlueprintProtocol
from dnd.character.blueprint.state import HasOtherEquipment
from dnd.character.delta.delta import Delta
from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)
from pydantic import Field


class OtherEquipmentDelta(Delta):
    """Delta produced when EquipmentAdder appends an item."""

    delta_type: Literal["OtherEquipmentDelta"] = "OtherEquipmentDelta"
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


class EquipmentAdder(BuildingBlock):
    """Adds an item to the character's other equipment list."""

    type: Literal[BuildingBlockType.EQUIPMENT_ADDER] = BuildingBlockType.EQUIPMENT_ADDER

    item: str = Field(description="Equipment item to add to character's inventory")

    @overload
    def get_change[T: HasOtherEquipment](
        self, state: T
    ) -> Generator[
        OtherEquipmentDelta, None, ProtocolIntersection[T, HasOtherEquipment]
    ]: ...

    @overload
    @deprecated("Pass a state satisfying HasOtherEquipment for precise return typing")
    def get_change[T: BlueprintProtocol](
        self, state: T
    ) -> Generator[Delta, None, BlueprintProtocol]: ...

    def get_change[T: BlueprintProtocol](
        self, state: T
    ) -> Generator[Delta, None, BlueprintProtocol]:
        if not isinstance(state, HasOtherEquipment):
            raise TypeError(
                f"{type(self).__name__} requires HasOtherEquipment, got {type(state).__name__}"
            )
        delta = OtherEquipmentDelta(
            other_equipment=state.other_equipment + (self.item,)
        )
        yield delta
        return delta.apply(state)
