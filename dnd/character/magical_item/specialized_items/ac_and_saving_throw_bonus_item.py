from dnd.character.magical_item.item import MagicalItem


class ACAndSavingThrowBonusItem(MagicalItem):
    """Generic magical item that provides bonuses to both AC and saving throws.

    Examples: Cloak of Protection (+1 AC, +1 saves), Ring of Protection (+1 AC, +1 saves)
    """

    ac_bonus: int
    saving_throw_bonus: int
