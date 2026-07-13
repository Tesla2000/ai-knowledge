"""Base class for all magical item choosers."""

from abc import ABC
from abc import abstractmethod

from dnd.character.blueprint.building_blocks.building_block import BuildingBlock
from dnd.character.blueprint.states.state import _BPT
from dnd.character.magical_item.item import MagicalItem
from pydantic import ConfigDict
from pydantic import Field
from pydantic import NonNegativeInt


class MagicalItemChooserBase(BuildingBlock, ABC):
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
    def select_items(self, blueprint: _BPT) -> tuple[MagicalItem, ...]: ...

    def apply(self, blueprint: _BPT) -> _BPT:
        selected_items = self.select_items(blueprint)
        return blueprint.model_copy(
            update={"magical_items": blueprint.magical_items + selected_items}
        )
