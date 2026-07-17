from typing import ClassVar

from pydantic import BaseModel, ConfigDict, NonNegativeInt, PositiveInt

from dnd.character.actions._fight_resource import ResourceName

__all__ = ["ResourceName", "_FightResource"]


class _FightResource(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    name: ResourceName
    max_uses: PositiveInt
    remaining_uses: NonNegativeInt
