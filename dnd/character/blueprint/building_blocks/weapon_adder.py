from __future__ import annotations

from collections.abc import Generator
from typing import cast
from typing import TYPE_CHECKING

from typing_protocol_intersection import ProtocolIntersection

from dnd.character.blueprint.building_blocks.building_block import BuildingBlock
from dnd.character.blueprint.state import Blueprint
from dnd.character.blueprint.state import BlueprintProtocol
from dnd.character.blueprint.state import HasWeapons
from dnd.character.delta.delta import Delta
from dnd.choices.equipment_creation.weapons import WeaponName
from pydantic import Field


class WeaponsDelta(Delta):
    """Delta produced when WeaponAdder appends a weapon."""

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


class WeaponAdder[T: HasWeapons](BuildingBlock[T, WeaponsDelta, HasWeapons]):
    """Adds a weapon to the character's weapons list."""

    weapon: WeaponName = Field(description="Weapon to add to character's inventory")

    def get_change(
        self, state: T
    ) -> Generator[WeaponsDelta, None, ProtocolIntersection[T, HasWeapons]]:
        delta = WeaponsDelta(weapons=state.weapons + (self.weapon,))
        yield delta
        return delta.apply(state)
