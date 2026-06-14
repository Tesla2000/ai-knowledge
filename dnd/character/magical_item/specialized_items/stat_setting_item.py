from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dnd.character.blueprint.blueprint import Blueprint

from dnd.character.magical_item.item import MagicalItem
from dnd.character.stats import Stats
from dnd.choices.stats_creation.statistic import Statistic


class StatSettingItem(MagicalItem):
    """Generic magical item that sets a specific stat to a fixed value.

    Examples: Amulet of Health (CON=19), Gauntlets of Ogre Power (STR=19),
              Belt of Giant Strength variants (STR=21/23/25/27/29)
    """

    stat: Statistic  # e.g., Statistic.STRENGTH, Statistic.CONSTITUTION
    stat_value: int  # e.g., 19, 21, 23, etc.

    def assign_to(self, blueprint: Blueprint) -> Blueprint:
        """Set the specified stat to the fixed value."""
        stat_name = self.stat.value.lower()  # Convert Statistic.STRENGTH -> 'strength'
        new_stats = Stats(
            **{**blueprint.stats.model_dump(), stat_name: self.stat_value}
        )
        return type(blueprint)(
            stats=new_stats, magical_items=blueprint.magical_items + (self,)
        )
