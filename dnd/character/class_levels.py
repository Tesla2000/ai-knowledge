from collections.abc import Iterator
from typing import Any

from dnd.choices.class_creation.character_class import Class
from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import NonNegativeInt


class ClassLevels(BaseModel):
    """Flat class-level state. Each field holds the level in that class (0 = not taken)."""

    model_config = ConfigDict(frozen=True)

    wizard: Any = 0
    sorcerer: NonNegativeInt = 0
    fighter: NonNegativeInt = 0
    barbarian: NonNegativeInt = 0
    rogue: NonNegativeInt = 0
    cleric: NonNegativeInt = 0
    druid: NonNegativeInt = 0
    paladin: NonNegativeInt = 0
    ranger: NonNegativeInt = 0
    monk: NonNegativeInt = 0
    bard: NonNegativeInt = 0
    warlock: NonNegativeInt = 0
    artificer: NonNegativeInt = 0

    def total_level(self) -> int:
        return sum(self.model_dump().values())

    def get_level(self, class_: Class) -> int:
        return int(self.model_dump().get(class_.name.lower(), 0))

    def all_levels(self) -> Iterator[tuple[Class, int]]:
        for class_ in Class:
            level = self.get_level(class_)
            if level > 0:
                yield class_, level

    def __contains__(self, class_: object) -> bool:
        return isinstance(class_, Class) and self.get_level(class_) > 0

    def __getitem__(self, class_: Class) -> int:
        return self.get_level(class_)
