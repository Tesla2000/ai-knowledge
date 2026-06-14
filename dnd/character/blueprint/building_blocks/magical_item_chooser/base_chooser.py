"""Base class for all magical item choosers."""

from __future__ import annotations

from abc import ABC

from dnd.character.blueprint.blueprint import Blueprint
from dnd.character.blueprint.building_blocks.building_block import (
    BuildingBlock,
)
from dnd.character.magical_item.item import MagicalItem
from pydantic import ConfigDict
from pydantic import Field


class MagicalItemChooserBase(BuildingBlock, ABC):
    """Abstract base class for choosers that select magical items.

    Implementations must select magical items based on rarity counts:
    - n_common, n_uncommon, n_rare, etc.

    This base class provides a common type for both random choosers
    (RandomMagicalItemChooser) and holistic AI choosers (AIMagicalItemChooser).

    - RandomMagicalItemChooser: Selects items level-by-level
    - AIMagicalItemChooser: Selects all items in a single holistic LLM call

    Subclasses implement _get_change() to define selection logic.
    """

    model_config = ConfigDict(frozen=True)

    n_common: int = Field(
        default=0, description="Number of common magical items to select"
    )
    n_uncommon: int = Field(
        default=0, description="Number of uncommon magical items to select"
    )
    n_rare: int = Field(default=0, description="Number of rare magical items to select")
    n_very_rare: int = Field(
        default=0, description="Number of very rare magical items to select"
    )
    n_legendary: int = Field(
        default=0, description="Number of legendary magical items to select"
    )
    n_artifact: int = Field(
        default=0, description="Number of artifact magical items to select"
    )
    n_unique: int = Field(
        default=0, description="Number of unique magical items to select"
    )
    n_mistery: int = Field(
        default=0, description="Number of mystery magical items to select"
    )

    @staticmethod
    def _add_items(
        blueprint: Blueprint, selected_items: tuple[MagicalItem, ...]
    ) -> Blueprint:
        new_magical_items = blueprint.magical_items + tuple(selected_items)
        for magical_item in new_magical_items:
            diff = magical_item.assign_to(blueprint)
            blueprint = blueprint.add_diff(diff)
        return blueprint
