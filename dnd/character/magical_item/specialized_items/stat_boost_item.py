from dnd.character.magical_item.item import MagicalItem
from dnd.choices.stats_creation.statistic import Statistic


class StatBoostItem(MagicalItem):
    """Generic magical item that increases a specific stat by a fixed amount.

    Examples: Ioun Stone of Agility (DEX +2, max 20), Tome of Understanding (WIS +2, max 20)
    The boost respects both the item's specified cap and the character's stats_cup.
    """

    stat: Statistic
    boost_amount: int
    max_value: int | None = None
