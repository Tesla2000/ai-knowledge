from typing import Union

from dnd.character.blueprint.building_blocks.stats_builder.standard_array import (
    StandardArray,
)

AnyStatsBuilder = Union[StandardArray]

__all__ = [
    "StandardArray",
    "AnyStatsBuilder",
]
