from dnd.character.magical_item.item import MagicalItem
from dnd.choices.stats_creation.statistic import Statistic


class StatSettingItem(MagicalItem):
    """Generic magical item that sets a specific stat to a fixed value.

    Examples: Amulet of Health (CON=19), Gauntlets of Ogre Power (STR=19),
              Belt of Giant Strength variants (STR=21/23/25/27/29)
    """

    stat: Statistic
    stat_value: int
