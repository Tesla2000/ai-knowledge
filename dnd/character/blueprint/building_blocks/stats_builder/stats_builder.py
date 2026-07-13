from abc import ABC


from dnd.character.blueprint.building_blocks.building_block import BuildingBlock
from dnd.character.blueprint.building_blocks.stats_priority import StatsPriority
from pydantic import Field


class StatsBuilder(BuildingBlock, ABC):
    """Abstract base class for building character ability scores.

    Subclasses implement different methods of generating stats (standard array,
    rolling, point buy, etc.) based on a priority order.
    """

    stats_priority: StatsPriority = Field(
        description="Ability scores ranked by priority for stat assignment"
    )
