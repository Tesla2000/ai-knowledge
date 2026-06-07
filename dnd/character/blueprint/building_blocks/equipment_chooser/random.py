from __future__ import annotations

import random

from dnd.character.armor.names import ArmorName
from dnd.character.blueprint.blueprint import Blueprint
from dnd.character.blueprint.building_blocks.equipment_chooser.base import (
    EquipmentChooser,
)
from dnd.choices.equipment_creation.weapons import WeaponName


class RandomEquipmentChooser(EquipmentChooser):
    """Randomly selects equipment from available choices.

    For each equipment choice in the blueprint, randomly selects one option
    and categorizes it as a weapon, armor, or other equipment. Clears all
    equipment choices after selection.

    Example:
        >>> chooser = RandomEquipmentChooser()
        >>> # Randomly picks from equipment_choices and categorizes them
    """

    def get_change(self, blueprint: Blueprint) -> Blueprint:
        weapons, armors, others = [], [], []
        for options in blueprint.equipment_choices:
            choice = random.choice(options)
            if isinstance(choice, WeaponName):
                weapons.append(choice)
            elif isinstance(choice, ArmorName):
                armors.append(choice)
            else:
                others.append(choice)
        return Blueprint(
            equipment_choices=(),
            weapons=blueprint.weapons + tuple(weapons),
            armors=blueprint.armors + tuple(armors),
            other_equipment=blueprint.other_equipment + tuple(others),
        )
