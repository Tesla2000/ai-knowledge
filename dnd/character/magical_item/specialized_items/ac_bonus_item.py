from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dnd.character.blueprint.blueprint import Blueprint

from dnd.character.magical_item.item import MagicalItem


class ACBonusItem(MagicalItem):
    """Generic magical item that provides a bonus to Armor Class.

    Examples: Bracers of Defense (+2 AC), Ring of Protection (+1 AC)
    """

    ac_bonus: int  # e.g., 1, 2, 3

    def assign_to(self, blueprint: Blueprint) -> Blueprint:  # type: ignore[override]
        """Add AC bonus to character."""
        return type(blueprint)(
            ac_bonus=blueprint.ac_bonus + self.ac_bonus,
            magical_items=blueprint.magical_items + (self,),
        )
