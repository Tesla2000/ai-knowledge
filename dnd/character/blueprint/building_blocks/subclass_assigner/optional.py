from __future__ import annotations

from collections.abc import Generator
from typing import Literal
from typing import overload

from typing_extensions import deprecated
from typing_protocol_intersection import ProtocolIntersection

from dnd.character.blueprint.building_blocks.building_block import BuildingBlock
from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)
from dnd.character.blueprint.building_blocks.subclass_assigner.ai import (
    AISubclassAssigner,
)
from dnd.character.blueprint.building_blocks.subclass_assigner.base import (
    CanNotAssign,
    SubclassDelta,
    _SubclassT,
)
from dnd.character.blueprint.building_blocks.subclass_assigner.random import (
    RandomSubclassAssigner,
)
from dnd.character.blueprint.state import BlueprintProtocol
from dnd.character.blueprint.state import HasSubclasses
from dnd.character.delta.delta import Delta
from pydantic import Field


class OptionalSubclassAssigner(BuildingBlock):
    """Optionally assigns a subclass, gracefully handling cases where assignment is not possible.

    Wraps another subclass assigner and silently succeeds if the assignment would fail
    (e.g., character not high enough level for subclass selection).
    """

    type: Literal[BuildingBlockType.OPTIONAL_SUBCLASS_ASSIGNER] = (
        BuildingBlockType.OPTIONAL_SUBCLASS_ASSIGNER
    )

    assigner: RandomSubclassAssigner | AISubclassAssigner = Field(
        description="The subclass assigner strategy to use (random or AI)"
    )

    @overload
    def get_change[T: _SubclassT](
        self, state: T
    ) -> Generator[SubclassDelta, None, ProtocolIntersection[T, HasSubclasses]]: ...

    @overload
    @deprecated(
        "Pass a state satisfying HasClasses and HasSubclasses for precise return typing"
    )
    def get_change[T: BlueprintProtocol](
        self, state: T
    ) -> Generator[Delta, None, BlueprintProtocol]: ...

    def get_change[T: BlueprintProtocol](
        self, state: T
    ) -> Generator[Delta, None, BlueprintProtocol]:
        if not isinstance(state, _SubclassT):
            raise TypeError(
                f"{type(self).__name__} requires HasClasses and HasSubclasses, got {type(state).__name__}"
            )
        try:
            result = yield from self.assigner.get_change(state)
            return result
        except CanNotAssign:
            delta = SubclassDelta(subclasses=state.subclasses)
            yield delta
            return delta.apply(state)
