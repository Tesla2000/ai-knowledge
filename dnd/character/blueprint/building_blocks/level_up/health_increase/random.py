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


class HealthIncreaseRandom(HealthIncrease):
    """Random health increase strategy.

    Rolls a random value between 1 and the hit die size for non-first levels.
    First level always gets the maximum hit die value.

    Example:
        - d6 hit die: random 1-6 health per level (after first)
        - d8 hit die: random 1-8 health per level (after first)
        - d10 hit die: random 1-10 health per level (after first)
        - d12 hit die: random 1-12 health per level (after first)
    """

    type: Literal[BuildingBlockType.HEALTH_INCREASE_RANDOM] = (
        BuildingBlockType.HEALTH_INCREASE_RANDOM
    )

    def _get_hit_die_value(self, hit_die: HitDieSize) -> int:
        """Get random hit die value.

        Args:
            hit_die: The hit die for the class.

        Returns:
            Random value between 1 and hit_die size (inclusive).
        """
        return random.randint(1, hit_die.value)
