from dnd.character.magical_item.item import MagicalItem
from dnd.choices.stats_creation.statistic import Statistic


class StatAndCapBoostItem(MagicalItem):
    """Generic magical item that increases both a stat value and its maximum.

    Examples: Tome of Clear Thought (INT +2, max INT +2),
              Tome of Leadership and Influence (CHA +2, max CHA +2)

    Unlike StatBoostItem which respects an existing cap, this item raises the cap itself.
    """

    stat: Statistic
    boost_amount: int
