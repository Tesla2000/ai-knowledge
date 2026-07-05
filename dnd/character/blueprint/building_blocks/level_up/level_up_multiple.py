from __future__ import annotations

from collections.abc import Generator
from typing import Literal

from dnd.character.blueprint.building_blocks.building_block import (
    BuildingBlock,
)
from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)
from dnd.character.blueprint.building_blocks.level_up.level_up import (
    LevelUp,
)
from dnd.character.blueprint.state import BlueprintProtocol
from dnd.character.delta.delta import Delta
from pydantic import Field


class LevelUpMultiple(BuildingBlock):
    """Container for multiple level up operations.

    Combines multiple LevelUp building blocks to apply sequential level ups
    for different classes.
    """

    type: Literal[BuildingBlockType.LEVEL_UP_MULTIPLE] = (
        BuildingBlockType.LEVEL_UP_MULTIPLE
    )

    blocks: tuple[LevelUp, ...] = Field(
        description="Tuple of LevelUp blocks to apply sequentially",
    )

    def flatten(self) -> Generator[BuildingBlock]:
        for block in self.blocks:
            yield from block.flatten()

    def get_change(
        self, state: BlueprintProtocol
    ) -> Generator[Delta, None, BlueprintProtocol]:
        current: BlueprintProtocol = state
        for block in self.flatten():
            current = yield from block.get_change(current)
        return current
