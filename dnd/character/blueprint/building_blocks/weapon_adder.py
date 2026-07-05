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
from dnd.character.blueprint.state import HasWeapons
from dnd.character.delta.delta import Delta
from dnd.choices.equipment_creation.weapons import WeaponName
from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)
from pydantic import Field


class WeaponsDelta(Delta):
    """Delta produced when WeaponAdder appends a weapon."""

    delta_type: Literal["WeaponsDelta"] = "WeaponsDelta"
    weapons: tuple[WeaponName, ...]

    def apply[T: BlueprintProtocol](
        self, state: T
    ) -> ProtocolIntersection[T, HasWeapons]:

        if TYPE_CHECKING:

            class BlueprintWithWeapons(Blueprint):
                weapons: tuple[WeaponName, ...]

        else:

            class BlueprintWithWeapons(type(state)):
                weapons: tuple[WeaponName, ...]

        return cast(
            ProtocolIntersection[T, HasWeapons],
            BlueprintWithWeapons.model_validate(
                {**dict(state), "weapons": self.weapons}
            ),
        )


class WeaponAdder(BuildingBlock):
    """Adds a weapon to the character's weapons list."""

    type: Literal[BuildingBlockType.WEAPON_ADDER] = BuildingBlockType.WEAPON_ADDER

    weapon: WeaponName = Field(description="Weapon to add to character's inventory")

    @overload
    def get_change[T: HasWeapons](
        self, state: T
    ) -> Generator[WeaponsDelta, None, ProtocolIntersection[T, HasWeapons]]: ...

    @overload
    @deprecated("Pass a state satisfying HasWeapons for precise return typing")
    def get_change[T: BlueprintProtocol](
        self, state: T
    ) -> Generator[Delta, None, BlueprintProtocol]: ...

    def get_change[T: BlueprintProtocol](
        self, state: T
    ) -> Generator[Delta, None, BlueprintProtocol]:
        if not isinstance(state, HasWeapons):
            raise TypeError(
                f"{type(self).__name__} requires HasWeapons, got {type(state).__name__}"
            )
        delta = WeaponsDelta(weapons=state.weapons + (self.weapon,))
        yield delta
        return delta.apply(state)
