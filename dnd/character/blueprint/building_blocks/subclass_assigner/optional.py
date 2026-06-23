from __future__ import annotations

from collections.abc import Generator

from typing_protocol_intersection import ProtocolIntersection

from dnd.character.blueprint.building_blocks.building_block import BuildingBlock
from dnd.character.blueprint.building_blocks.subclass_assigner.ai import (
    AISubclassAssigner,
)
from dnd.character.blueprint.building_blocks.subclass_assigner.base import (
    CanNotAssign,
    SubclassDelta,
)
from dnd.character.blueprint.building_blocks.subclass_assigner.random import (
    RandomSubclassAssigner,
)
from dnd.character.blueprint.state import HasClasses
from dnd.character.blueprint.state import HasSubclasses
from pydantic import Field


class OptionalSubclassAssigner[T: ProtocolIntersection[HasClasses, HasSubclasses]](
    BuildingBlock[T, SubclassDelta, HasSubclasses]
):
    """Optionally assigns a subclass, gracefully handling cases where assignment is not possible.

    Wraps another subclass assigner and silently succeeds if the assignment would fail
    (e.g., character not high enough level for subclass selection).
    """

    assigner: RandomSubclassAssigner[T] | AISubclassAssigner[T] = Field(
        description="The subclass assigner strategy to use (random or AI)"
    )

    def get_change(
        self, state: T
    ) -> Generator[SubclassDelta, None, ProtocolIntersection[T, HasSubclasses]]:
        try:
            result = yield from self.assigner.get_change(state)
            return result
        except CanNotAssign:
            delta = SubclassDelta(subclasses=state.subclasses)
            yield delta
            return delta.apply(state)
