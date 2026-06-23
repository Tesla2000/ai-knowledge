from __future__ import annotations

from collections.abc import Generator
from typing import ClassVar
from typing import cast
from typing import TYPE_CHECKING

from typing_protocol_intersection import ProtocolIntersection

from dnd.character.blueprint.state import Blueprint
from dnd.character.blueprint.state import BlueprintProtocol
from dnd.character.blueprint.state import HasStats
from dnd.character.blueprint.building_blocks.stats_builder.stats_builder import (
    StatsBuilder,
)
from dnd.character.delta.delta import Delta
from dnd.character.stats import Stats


class StatsDelta(Delta):
    """Delta produced when StatsBuilder sets character stats."""

    stats: Stats

    def apply[T: BlueprintProtocol](
        self, state: T
    ) -> ProtocolIntersection[T, HasStats]:

        if TYPE_CHECKING:

            class BlueprintWithStats(Blueprint):
                stats: Stats

        else:

            class BlueprintWithStats(type(state)):
                stats: Stats

        return cast(
            ProtocolIntersection[T, HasStats],
            BlueprintWithStats.model_validate({**dict(state), "stats": self.stats}),
        )


class StandardArray[T: BlueprintProtocol](StatsBuilder[T]):
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

    def get_change(
        self, state: T
    ) -> Generator[StatsDelta, None, ProtocolIntersection[T, HasStats]]:
        delta = StatsDelta(
            stats=Stats.from_mapping(
                dict(zip(self.stats_priority, self._standard_array_descending))
            )
        )
        yield delta
        return delta.apply(state)
