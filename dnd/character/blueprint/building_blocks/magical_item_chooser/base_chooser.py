"""Base class for all magical item choosers."""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from collections.abc import Generator

from dnd.character.blueprint.building_blocks.building_block import BuildingBlock
from dnd.character.blueprint.state import BlueprintProtocol
from dnd.character.blueprint.state import HasMagicalItems
from dnd.character.delta.magical_items_delta import MagicalItemsDelta
from dnd.character.magical_item.item import MagicalItem
from pydantic import ConfigDict
from pydantic import Field
from pydantic import NonNegativeInt


class MagicalItemChooserBase(
    BuildingBlock[BlueprintProtocol, MagicalItemsDelta, HasMagicalItems], ABC
):
    """Abstract base class for choosers that select magical items.

    Implementations must select magical items based on rarity counts:
    - n_common, n_uncommon, n_rare, etc.
    """

    model_config = ConfigDict(frozen=True)

    n_common: NonNegativeInt = Field(
        default=0, description="Number of common magical items to select"
    )
    n_uncommon: NonNegativeInt = Field(
        default=0, description="Number of uncommon magical items to select"
    )
    n_rare: NonNegativeInt = Field(
        default=0, description="Number of rare magical items to select"
    )
    n_very_rare: NonNegativeInt = Field(
        default=0, description="Number of very rare magical items to select"
    )
    n_legendary: NonNegativeInt = Field(
        default=0, description="Number of legendary magical items to select"
    )
    n_artifact: NonNegativeInt = Field(
        default=0, description="Number of artifact magical items to select"
    )
    n_unique: NonNegativeInt = Field(
        default=0, description="Number of unique magical items to select"
    )
    n_mistery: NonNegativeInt = Field(
        default=0, description="Number of mystery magical items to select"
    )

    @abstractmethod
    def _select_items(self, state: BlueprintProtocol) -> tuple[MagicalItem, ...]: ...

    def get_change(
        self, state: BlueprintProtocol
    ) -> Generator[MagicalItemsDelta, None, HasMagicalItems]:
        selected_items = self._select_items(state)
        existing = state.magical_items if isinstance(state, HasMagicalItems) else ()
        delta = MagicalItemsDelta(magical_items=existing + selected_items)
        yield delta
        return delta.apply(state)
