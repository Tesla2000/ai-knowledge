"""Random subclass assigner for character creation."""

from __future__ import annotations

import random
from collections.abc import Generator

from typing_protocol_intersection import ProtocolIntersection

from dnd.character.blueprint.building_blocks.building_block import BuildingBlock
from dnd.character.blueprint.building_blocks.subclass_assigner.base import (
    SubclassDelta,
)
from dnd.character.blueprint.building_blocks.subclass_assigner.base import (
    _check_can_assign,
)
from dnd.character.blueprint.state import HasClasses
from dnd.character.blueprint.state import HasSubclasses
from dnd.choices.class_creation.character_class import AnySubclass
from dnd.choices.class_creation.character_class import Class
from dnd.choices.class_creation.character_class import SUBCLASSES
from pydantic import ConfigDict
from pydantic import Field


class RandomSubclassAssigner[T: ProtocolIntersection[HasClasses, HasSubclasses]](
    BuildingBlock[T, SubclassDelta, HasSubclasses]
):
    """Randomly selects a subclass from the valid subclasses for the given class.

    Provides deterministic randomness when seed is set, useful for
    reproducible character generation.

    Example:
        >>> from dnd.choices.class_creation.character_class import Class
        >>> assigner = RandomSubclassAssigner(
        ...     class_=Class.WIZARD,
        ...     seed=42  # Reproducible
        ... )
        >>> # or
        >>> assigner = RandomSubclassAssigner(class_=Class.WIZARD)  # Truly random
    """

    model_config = ConfigDict(frozen=True)

    class_: Class = Field(
        description="The character class for which to assign a subclass"
    )
    seed: int | None = Field(
        default=None,
        description="Optional seed for reproducible random selection",
    )

    def get_change(
        self, state: T
    ) -> Generator[SubclassDelta, None, ProtocolIntersection[T, HasSubclasses]]:
        _check_can_assign(self.class_, state)
        subclass_enum = SUBCLASSES[self.class_]
        for existing in state.subclasses:
            if isinstance(existing, subclass_enum):
                delta = SubclassDelta(subclasses=state.subclasses)
                yield delta
                return delta.apply(state)
        random.seed(self.seed)
        selected: AnySubclass = random.choice(tuple(subclass_enum))
        delta = SubclassDelta(subclasses=state.subclasses + (selected,))
        yield delta
        return delta.apply(state)
