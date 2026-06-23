from dnd.character.magical_item.item import MagicalItem


class ACBonusItem(MagicalItem):
    """Generic magical item that provides a bonus to Armor Class.

    Examples: Bracers of Defense (+2 AC), Ring of Protection (+1 AC)
    """

    ac_bonus: int
