from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dnd.character.blueprint.blueprint import Blueprint

from dnd.character.magical_item.item import MagicalItem
from dnd.character.stats import Stats


class ACAndSavingThrowBonusItem(MagicalItem):
    """Generic magical item that provides bonuses to both AC and saving throws.

    Examples: Cloak of Protection (+1 AC, +1 saves), Ring of Protection (+1 AC, +1 saves)
    """

    ac_bonus: int
    saving_throw_bonus: int

    def assign_to(self, blueprint: Blueprint) -> Blueprint:
        """Add bonuses to AC and all saving throws."""
        new_saving_throws = Stats(
            **{
                k: v + self.saving_throw_bonus
                for k, v in blueprint.saving_throw_bonuses.model_dump().items()
            }
        )
        return type(blueprint)(
            ac_bonus=blueprint.ac_bonus + self.ac_bonus,
            saving_throw_bonuses=new_saving_throws,
            magical_items=blueprint.magical_items + (self,),
        )
