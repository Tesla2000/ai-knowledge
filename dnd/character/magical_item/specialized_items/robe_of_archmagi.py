from dnd.character.armor.armor import Armor
from dnd.character.armor.category import ArmorCategory
from dnd.character.armor.names import ArmorName
from dnd.character.character import Character
from dnd.character.magical_item.item import MagicalItem
from dnd.choices.stats_creation.statistic import Statistic
from pydantic import PositiveInt


class RobeOfTheArchmagi(MagicalItem, Armor):
    """Legendary robe granting +2 spellcasting bonus and 15 + DEX mod AC for arcane casters."""

    name: ArmorName = ArmorName.ROBE_OF_THE_ARCHMAGI
    category: ArmorCategory = ArmorCategory.NONE
    cost: PositiveInt = 15000
    disadvantage_on_stealth: bool = False
    base_ac: int = 15

    def calc_ac(self, character: Character) -> int:
        return self.base_ac + character.stats.get_modifier(Statistic.DEXTERITY)
