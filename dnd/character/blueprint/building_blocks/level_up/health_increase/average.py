from __future__ import annotations

from dnd.character.blueprint.building_blocks.level_up.health_increase.base import (
    HealthIncrease,
)
from dnd.choices.equipment_creation.weapons import HitDieSize
from typing import Literal
from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)


class HealthIncreaseAverage(HealthIncrease):
    """Fixed health increase strategy.

    Uses the average value of the hit die (hit_die // 2 + 1) for non-first levels.
    First level always gets the maximum hit die value.

    Example:
        - d6 hit die: +4 health per level (after first)
        - d8 hit die: +5 health per level (after first)
        - d10 hit die: +6 health per level (after first)
        - d12 hit die: +7 health per level (after first)
    """

    type: Literal[BuildingBlockType.HEALTH_INCREASE_AVERAGE] = (
        BuildingBlockType.HEALTH_INCREASE_AVERAGE
    )

    def _get_hit_die_value(self, hit_die: HitDieSize) -> int:
        """Get fixed hit die value (average roll).

        Args:
            hit_die: The hit die for the class.

        Returns:
            Average value: hit_die // 2 + 1
        """
        return hit_die.value // 2 + 1
