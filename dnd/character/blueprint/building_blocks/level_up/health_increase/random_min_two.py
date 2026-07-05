from __future__ import annotations

import random

from dnd.character.blueprint.building_blocks.level_up.health_increase.base import (
    HealthIncrease,
)
from dnd.choices.equipment_creation.weapons import HitDieSize
from typing import Literal
from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)


class HealthIncreaseRandomMinTwo(HealthIncrease):
    """Random health increase strategy with minimum value of 2.

    Rolls a random value between 2 and the hit die size.
    First level always gets the maximum hit die value.

    Example:
        - d6 hit die: random 2-6
        - d8 hit die: random 2-8
        - d10 hit die: random 2-10
        - d12 hit die: random 2-12
    """

    type: Literal[BuildingBlockType.HEALTH_INCREASE_RANDOM_MIN_TWO] = (
        BuildingBlockType.HEALTH_INCREASE_RANDOM_MIN_TWO
    )

    def _get_hit_die_value(self, hit_die: HitDieSize) -> int:
        """Get random hit die value, minimum 2.

        Args:
            hit_die: The hit die for the class.

        Returns:
            Random value between 2 and hit_die size (inclusive).
        """
        return random.randint(2, hit_die.value)
