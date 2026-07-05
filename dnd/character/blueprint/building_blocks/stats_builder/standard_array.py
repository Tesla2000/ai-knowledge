from __future__ import annotations

from collections.abc import Generator
from typing import Literal
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
from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)


class StatsDelta(Delta):
    """Delta produced when StatsBuilder sets character stats."""

    delta_type: Literal["StatsDelta"] = "StatsDelta"
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


class StandardArray(StatsBuilder):
    """Assigns ability scores using the standard array method (15, 14, 13, 12, 10, 8).

    Distributes the standard D&D 5e ability score array to the six ability scores
    based on the provided stats priority, assigning higher values to more important stats.

    Example:
        >>> stats_priority = StatsPriority((Statistic.STR, Statistic.CON, ...))
        >>> builder = StandardArray(stats_priority=stats_priority)
        >>> # Will assign 15 to STR, 14 to CON, etc.
    """

    type: Literal[BuildingBlockType.STANDARD_ARRAY] = BuildingBlockType.STANDARD_ARRAY

    _standard_array_descending: ClassVar[tuple[int, int, int, int, int, int]] = (
        15,
        14,
        13,
        12,
        10,
        8,
    )

    def get_change[T: BlueprintProtocol](
        self, state: T
    ) -> Generator[StatsDelta, None, ProtocolIntersection[T, HasStats]]:
        delta = StatsDelta(
            stats=Stats.from_mapping(
                dict(zip(self.stats_priority, self._standard_array_descending))
            )
        )
        yield delta
        return delta.apply(state)
