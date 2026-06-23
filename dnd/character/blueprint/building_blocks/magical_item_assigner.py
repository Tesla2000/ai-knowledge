from __future__ import annotations

from collections.abc import Generator

from dnd.character.blueprint.building_blocks.building_block import BuildingBlock
from dnd.character.blueprint.state import BlueprintProtocol
from dnd.character.blueprint.state import HasMagicalItems
from dnd.character.delta.magical_items_delta import MagicalItemsDelta
from dnd.character.magical_item.item import MagicalItem
from pydantic import Field


class MagicalItemAssigner(
    BuildingBlock[BlueprintProtocol, MagicalItemsDelta, HasMagicalItems]
):
    """Building block that assigns a magical item to a character blueprint."""

    magical_item: MagicalItem = Field(
        description="Magical item to assign to the character"
    )

    def get_change(
        self, state: BlueprintProtocol
    ) -> Generator[MagicalItemsDelta, None, HasMagicalItems]:
        existing = state.magical_items if isinstance(state, HasMagicalItems) else ()
        delta = MagicalItemsDelta(magical_items=existing + (self.magical_item,))
        yield delta
        return delta.apply(state)
