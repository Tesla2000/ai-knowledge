from __future__ import annotations

from typing import TYPE_CHECKING
from typing import TypeVar

from pydantic import BaseModel

if TYPE_CHECKING:
    from dnd.character.blueprint.blueprint import Blueprint
from dnd.character.magical_item.level import Level
from dnd.character.magical_item.source import Source

BlueprintType = TypeVar("BlueprintType", bound="Blueprint")


class MagicalItem(BaseModel):
    name: str
    description: str
    level: Level
    source: Source
    attuned: bool

    def assign_to(self, blueprint: BlueprintType) -> BlueprintType:
        return type(blueprint)(magical_items=blueprint.magical_items + (self,))
