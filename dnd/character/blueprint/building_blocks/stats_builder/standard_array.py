from __future__ import annotations

from typing import ClassVar

from dnd.character.blueprint.blueprint import Blueprint
from dnd.character.blueprint.building_blocks.stats_builder.stats_builder import (
    StatsBuilder,
)
from dnd.character.stats import Stats


class StandardArray(StatsBuilder):
    """Assigns ability scores using the standard array method (15, 14, 13, 12, 10, 8).

    Distributes the standard D&D 5e ability score array to the six ability scores
    based on the provided stats priority, assigning higher values to more important stats.

    Example:
        >>> stats_priority = StatsPriority((Statistic.STR, Statistic.CON, ...))
        >>> builder = StandardArray(stats_priority=stats_priority)
        >>> # Will assign 15 to STR, 14 to CON, etc.
    """

    _standard_array_descending: ClassVar[tuple[int, int, int, int, int, int]] = (
        15,
        14,
        13,
        12,
        10,
        8,
    )

    def get_change(self, blueprint: Blueprint) -> Blueprint:
        return Blueprint(
            stats=Stats.from_mapping(
                dict(zip(self.stats_priority, self._standard_array_descending))
            )
        )
