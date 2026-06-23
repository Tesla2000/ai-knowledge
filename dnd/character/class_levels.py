from __future__ import annotations

from collections.abc import Iterator

from dnd.choices.class_creation.character_class import Class
from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import PositiveInt


class ClassLevels(BaseModel):
    """Accumulating class level state during construction.

    Starts empty; class levels are added by deltas via dynamic subclass
    creation (mirroring how Blueprint grows via HasRace, HasStats, etc.).
    Use isinstance(state, HasWizardLevel) on the blueprint state to check
    if a class has been leveled up.
    """

    model_config = ConfigDict(frozen=True)

    def total_level(self) -> int:
        return sum(self.model_dump().values())

    def get_level(self, class_: Class) -> int:
        return dict(self.all_levels()).get(class_, 0)

    def all_levels(self) -> Iterator[tuple[Class, PositiveInt]]:
        _field_to_class: dict[str, Class] = {c.name.lower(): c for c in Class}
        for field_name, value in self.model_dump().items():
            yield _field_to_class[field_name], value
