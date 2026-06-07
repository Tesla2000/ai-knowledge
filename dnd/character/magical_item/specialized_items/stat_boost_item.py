from __future__ import annotations

from typing import Optional
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dnd.character.blueprint.blueprint import Blueprint

from dnd.character.magical_item.item import MagicalItem
from dnd.character.stats import Stats
from dnd.choices.stats_creation.statistic import Statistic


class StatBoostItem(MagicalItem):
    """Generic magical item that increases a specific stat by a fixed amount.

    Examples: Ioun Stone of Agility (DEX +2, max 20), Tome of Understanding (WIS +2, max 20)
    The boost respects both the item's specified cap and the character's stats_cup.
    """

    stat: Statistic  # e.g., Statistic.STRENGTH, Statistic.DEXTERITY
    boost_amount: int  # e.g., 2
    max_value: Optional[int] = None  # e.g., 20 (if None, uses stats_cup)

    def assign_to(self, blueprint: Blueprint) -> Blueprint:
        """Increase the specified stat by the boost amount, respecting the maximum."""
        stat_name = (
            self.stat.value.lower()
        )  # Convert Statistic.STRENGTH -> 'strength'

        # Get current stat value and cap
        current_value = getattr(blueprint.stats, stat_name)
        stats_cup_value = getattr(blueprint.stats_cup, stat_name)

        # Determine the effective cap
        effective_cap = (
            self.max_value if self.max_value is not None else stats_cup_value
        )

        # Calculate new value: add boost, but don't exceed the cap
        new_value = min(current_value + self.boost_amount, effective_cap)

        new_stats = Stats(
            **{**blueprint.stats.model_dump(), stat_name: new_value}
        )

        return type(blueprint)(
            stats=new_stats, magical_items=blueprint.magical_items + (self,)
        )
