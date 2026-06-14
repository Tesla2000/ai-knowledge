from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dnd.character.blueprint.blueprint import Blueprint

from dnd.character.magical_item.item import MagicalItem
from dnd.character.stats import Stats
from dnd.choices.stats_creation.statistic import Statistic


class StatAndCapBoostItem(MagicalItem):
    """Generic magical item that increases both a stat value and its maximum.

    Examples: Tome of Clear Thought (INT +2, max INT +2),
              Tome of Leadership and Influence (CHA +2, max CHA +2)

    Unlike StatBoostItem which respects an existing cap, this item raises the cap itself.
    """

    stat: Statistic  # e.g., Statistic.INTELLIGENCE, Statistic.CHARISMA
    boost_amount: int  # e.g., 2

    def assign_to(self, blueprint: Blueprint) -> Blueprint:
        """Increase both the stat value and its maximum by the boost amount."""
        stat_name = (
            self.stat.value.lower()
        )  # Convert Statistic.INTELLIGENCE -> 'intelligence'

        # Get current stat value and cap
        current_value = blueprint.stats.get_stat(self.stat)
        current_cap = blueprint.stats_cup.get_stat(self.stat)

        # Increase both the stat and its maximum
        new_value = current_value + self.boost_amount
        new_cap = current_cap + self.boost_amount

        new_stats = Stats(**{**blueprint.stats.model_dump(), stat_name: new_value})

        new_stats_cup = Stats(
            **{**blueprint.stats_cup.model_dump(), stat_name: new_cap}
        )

        return type(blueprint)(
            stats=new_stats,
            stats_cup=new_stats_cup,
            magical_items=blueprint.magical_items + (self,),
        )
