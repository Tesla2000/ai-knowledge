"""Random subclass assigner for character creation."""

from __future__ import annotations

import random
from collections.abc import Generator
from typing import Literal
from typing import cast
from typing import overload

from typing_extensions import deprecated
from typing_protocol_intersection import ProtocolIntersection

from dnd.character.blueprint.building_blocks.building_block import BuildingBlock
from dnd.character.blueprint.building_blocks.subclass_assigner.base import (
    SubclassDelta,
    _SubclassT,
)
from dnd.character.blueprint.building_blocks.subclass_assigner.base import (
    _check_can_assign,
)
from dnd.character.blueprint.state import BlueprintProtocol
from dnd.character.blueprint.state import HasSubclasses
from dnd.character.delta.delta import Delta
from dnd.choices.class_creation.character_class import AnySubclass
from dnd.choices.class_creation.character_class import Class
from dnd.choices.class_creation.character_class import SUBCLASSES
from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)
from pydantic import ConfigDict
from pydantic import Field


class RandomSubclassAssigner(BuildingBlock):
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

    type: Literal[BuildingBlockType.RANDOM_SUBCLASS_ASSIGNER] = (
        BuildingBlockType.RANDOM_SUBCLASS_ASSIGNER
    )

    model_config = ConfigDict(frozen=True)

    class_: Class = Field(
        description="The character class for which to assign a subclass"
    )
    seed: int | None = Field(
        default=None,
        description="Optional seed for reproducible random selection",
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
        _check_can_assign(self.class_, state)
        subclass_enum = SUBCLASSES[self.class_]
        for existing in state.subclasses:
            if isinstance(existing, subclass_enum):
                delta = SubclassDelta(subclasses=state.subclasses)
                yield delta
                return delta.apply(state)
        random.seed(self.seed)
        selected = cast(AnySubclass, random.choice(tuple(subclass_enum)))
        delta = SubclassDelta(subclasses=state.subclasses + (selected,))
        yield delta
        return delta.apply(state)
