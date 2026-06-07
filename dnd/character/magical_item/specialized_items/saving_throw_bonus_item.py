from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dnd.character.blueprint.blueprint import Blueprint

from dnd.character.magical_item.item import MagicalItem
from dnd.character.stats import Stats


class SavingThrowBonusItem(MagicalItem):
    """Generic magical item that provides bonuses to saving throws.

    Examples: Cloak of Protection (+1 all saves), Ring of Protection (+1 all saves)
    """

    saving_throw_bonus: int  # e.g., 1, 2, 3

    def assign_to(self, blueprint: Blueprint) -> Blueprint:
        """Add bonus to all saving throws."""
        new_saving_throws = Stats(
            **{
                k: v + self.saving_throw_bonus
                for k, v in blueprint.saving_throw_bonuses.model_dump().items()
            }
        )
        return type(blueprint)(
            saving_throw_bonuses=new_saving_throws,
            magical_items=blueprint.magical_items + (self,),
        )
