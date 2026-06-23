from __future__ import annotations

import random

from dnd.character.armor.names import ArmorName
from dnd.character.blueprint.building_blocks.equipment_chooser.base import (
    EquipmentChooser,
)
from dnd.character.blueprint.state import HasEquipmentChoices
from dnd.choices.equipment_creation.weapons import WeaponName


class RandomEquipmentChooser[T: HasEquipmentChoices](EquipmentChooser[T]):
    """Randomly selects equipment from available choices.

    For each equipment choice in the blueprint, randomly selects one option
    and categorizes it as a weapon, armor, or other equipment. Clears all
    equipment choices after selection.

    Example:
        >>> chooser = RandomEquipmentChooser()
        >>> # Randomly picks from equipment_choices and categorizes them
    """

    def _pick_equipment(
        self, state: T
    ) -> tuple[list[WeaponName], list[ArmorName], list[str]]:
        weapons: list[WeaponName] = []
        armors: list[ArmorName] = []
        others: list[str] = []
        for options in state.equipment_choices:
            choice = random.choice(options)
            if isinstance(choice, WeaponName):
                weapons.append(choice)
            elif isinstance(choice, ArmorName):
                armors.append(choice)
            else:
                others.append(str(choice))
        return weapons, armors, others
