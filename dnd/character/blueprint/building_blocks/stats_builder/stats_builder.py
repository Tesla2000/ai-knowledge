from __future__ import annotations

from abc import ABC


from dnd.character.blueprint.building_blocks.building_block import BuildingBlock
from dnd.character.blueprint.building_blocks.stats_priority import StatsPriority
from dnd.character.blueprint.state import BlueprintProtocol
from dnd.character.blueprint.state import HasStats
from dnd.character.delta.delta import Delta
from pydantic import Field


class StatsBuilder[T: BlueprintProtocol](BuildingBlock[T, Delta, HasStats], ABC):
    """Abstract base class for building character ability scores.

    Subclasses implement different methods of generating stats (standard array,
    rolling, point buy, etc.) based on a priority order.
    """

    stats_priority: StatsPriority = Field(
        description="Ability scores ranked by priority for stat assignment"
    )
