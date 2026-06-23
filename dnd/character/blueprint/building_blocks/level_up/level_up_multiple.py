from __future__ import annotations

from dnd.character.blueprint.building_blocks import (
    CombinedBlock,
)
from dnd.character.blueprint.building_blocks.level_up.level_up import (
    LevelUp,
)
from pydantic import Field


class LevelUpMultiple(CombinedBlock):
    """Container for multiple level up operations.

    Combines multiple LevelUp building blocks to apply sequential level ups
    for different classes.
    """

    blocks: tuple[LevelUp, ...] = Field(
        description="Tuple of LevelUp blocks to apply sequentially",
    )
