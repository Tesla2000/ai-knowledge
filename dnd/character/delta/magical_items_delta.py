from __future__ import annotations

from typing import cast
from typing import TYPE_CHECKING

from typing_protocol_intersection import ProtocolIntersection

from dnd.character.blueprint.state import Blueprint
from dnd.character.blueprint.state import BlueprintProtocol
from dnd.character.blueprint.state import HasMagicalItems
from dnd.character.delta.delta import Delta
from dnd.character.magical_item.item import MagicalItem


class MagicalItemsDelta(Delta):
    """Delta produced when a magical item is added to the character."""

    magical_items: tuple[MagicalItem, ...]

    def apply[T: BlueprintProtocol](
        self, state: T
    ) -> ProtocolIntersection[T, HasMagicalItems]:
        if TYPE_CHECKING:

            class BlueprintWithMagicalItems(Blueprint):
                magical_items: tuple[MagicalItem, ...]

        else:

            class BlueprintWithMagicalItems(type(state)):
                magical_items: tuple[MagicalItem, ...]

        return cast(
            ProtocolIntersection[T, HasMagicalItems],
            BlueprintWithMagicalItems.model_validate(
                dict(state) | {"magical_items": self.magical_items}
            ),
        )
