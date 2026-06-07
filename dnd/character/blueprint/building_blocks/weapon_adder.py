from __future__ import annotations

from dnd.character.blueprint.blueprint import Blueprint
from dnd.character.blueprint.building_blocks.building_block import (
    BuildingBlock,
)
from dnd.choices.equipment_creation.weapons import WeaponName
from pydantic import Field


class WeaponAdder(BuildingBlock):
    """Adds a weapon to the character's weapons list.

    Appends to existing weapons. Allows duplicates (e.g., multiple daggers).

    Example:
        >>> builder = Builder([
        ...     WeaponAdder(weapon=WeaponName.LONGSWORD),
        ...     WeaponAdder(weapon=WeaponName.DAGGER),
        ...     WeaponAdder(weapon=WeaponName.DAGGER),  # Second dagger
        ... ])  # Character will have longsword and 2 daggers
    """

    weapon: WeaponName = Field(
        description="Weapon to add to character's inventory"
    )

    def get_change(self, blueprint: Blueprint) -> Blueprint:
        """Add the weapon to the existing weapons tuple.

        Args:
            blueprint: The current blueprint state.

        Yields:
            Blueprint with the weapon added.
        """
        existing_weapons = blueprint.weapons
        new_weapons = existing_weapons + (self.weapon,)
        return Blueprint(weapons=new_weapons)
