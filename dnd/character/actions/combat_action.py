from typing import Annotated

from pydantic import Field

from dnd.character.actions._base_action import (
    Action,
    BaseAction,
    BonusAction,
    CombatAction,
)
from dnd.character.actions.attack_with_axe import AttackWithAxe
from dnd.character.actions.use_rage import UseRage

AnyCombatAction = Annotated[
    AttackWithAxe | UseRage,
    Field(discriminator="name"),
]

__all__ = [
    "Action",
    "AnyCombatAction",
    "AttackWithAxe",
    "BaseAction",
    "BonusAction",
    "CombatAction",
    "UseRage",
]
