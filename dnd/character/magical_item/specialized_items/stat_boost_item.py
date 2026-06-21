from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dnd.character.blueprint.blueprint import Blueprint

from dnd.character.magical_item.item import MagicalItem
from dnd.choices.stats_creation.statistic import Statistic


class StatBoostItem(MagicalItem):
    """Generic magical item that increases a specific stat by a fixed amount.

    Examples: Ioun Stone of Agility (DEX +2, max 20), Tome of Understanding (WIS +2, max 20)
    The boost respects both the item's specified cap and the character's stats_cup.
    """

    stat: Statistic  # e.g., Statistic.STRENGTH, Statistic.DEXTERITY
    boost_amount: int  # e.g., 2
    max_value: int | None = None  # e.g., 20 (if None, uses stats_cup)

    def assign_to(self, blueprint: Blueprint) -> Blueprint:  # type: ignore[override]
        """Increase the specified stat by the boost amount, respecting the maximum."""
        if blueprint.stats is None:
            raise ValueError("Blueprint has no stats assigned yet")

        current_value = blueprint.stats.get_stat(self.stat)
        stats_cup_value = blueprint.stats_cup.get_stat(self.stat)

        effective_cap = (
            self.max_value if self.max_value is not None else stats_cup_value
        )

        new_value = min(current_value + self.boost_amount, effective_cap)
        new_stats = blueprint.stats.with_stat(self.stat, new_value)

        return type(blueprint)(
            stats=new_stats, magical_items=blueprint.magical_items + (self,)
        )
