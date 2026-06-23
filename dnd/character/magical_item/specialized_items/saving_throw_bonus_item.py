from dnd.character.magical_item.item import MagicalItem


class SavingThrowBonusItem(MagicalItem):
    """Generic magical item that provides bonuses to saving throws.

    Examples: Cloak of Protection (+1 all saves), Ring of Protection (+1 all saves)
    """

    saving_throw_bonus: int
