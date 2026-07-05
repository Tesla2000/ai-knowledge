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


class HealthIncreaseRandomRerollOnes(HealthIncrease):
    """Random health increase strategy with reroll on 1.

    Rolls a random value between 1 and the hit die size.
    If a 1 is rolled, reroll once and take the new value.
    First level always gets the maximum hit die value.

    Example:
        - d6 hit die: random 1-6, reroll if 1
        - d8 hit die: random 1-8, reroll if 1
        - d10 hit die: random 1-10, reroll if 1
        - d12 hit die: random 1-12, reroll if 1
    """

    type: Literal[BuildingBlockType.HEALTH_INCREASE_RANDOM_REROLL_ONES] = (
        BuildingBlockType.HEALTH_INCREASE_RANDOM_REROLL_ONES
    )

    def _get_hit_die_value(self, hit_die: HitDieSize) -> int:
        """Get random hit die value, rerolling 1s once.

        Args:
            hit_die: The hit die for the class.

        Returns:
            Random value between 1 and hit_die size. If 1 is rolled,
            reroll once and use the new value.
        """
        roll = random.randint(1, hit_die.value)
        if roll == 1:
            roll = random.randint(1, hit_die.value)
        return roll
