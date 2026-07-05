"""Random magical item selection."""

from __future__ import annotations

import random

from dnd.character.blueprint.building_blocks.magical_item_chooser.base_chooser import (
    MagicalItemChooserBase,
)
from dnd.character.blueprint.state import BlueprintProtocol
from dnd.character.magical_item.item import MagicalItem
from dnd.character.magical_item.items import MAGICAL_ITEMS
from dnd.character.magical_item.level import Level
from typing import Literal
from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)
from pydantic import ConfigDict
from pydantic import Field


class RandomMagicalItemChooser(MagicalItemChooserBase):
    """Randomly selects magical items by rarity level.

    Selects items level-by-level using random.choices(), allowing duplicates.
    Optionally accepts a seed for reproducible selection.

    Example:
        >>> chooser = RandomMagicalItemChooser(
        ...     n_uncommon=2,
        ...     n_rare=1,
        ...     seed=42,
        ... )
        >>> builder = Builder().add(chooser)
    """

    type: Literal[BuildingBlockType.RANDOM_MAGICAL_ITEM_CHOOSER] = (
        BuildingBlockType.RANDOM_MAGICAL_ITEM_CHOOSER
    )

    model_config = ConfigDict(frozen=True)

    seed: int | None = Field(
        default=None,
        description="Optional seed for reproducible random selection",
    )

    def _select_items(self, state: BlueprintProtocol) -> tuple[MagicalItem, ...]:
        level_counts = {
            Level.COMMON: self.n_common,
            Level.UNCOMMON: self.n_uncommon,
            Level.RARE: self.n_rare,
            Level.VERY_RARE: self.n_very_rare,
            Level.LEGENDARY: self.n_legendary,
            Level.ARTIFACT: self.n_artifact,
            Level.UNIQUE: self.n_unique,
            Level.MISTERY: self.n_mistery,
        }

        selected_items: list[MagicalItem] = []

        for level, count in level_counts.items():
            if count > 0:
                available = [item for item in MAGICAL_ITEMS if item.level == level]

                if not available:
                    raise ValueError(
                        f"No {level.value} magical items available in the item database."
                    )

                random.seed(self.seed)
                selected = random.choices(available, k=count)
                selected_items.extend(selected)

        return tuple(selected_items)
