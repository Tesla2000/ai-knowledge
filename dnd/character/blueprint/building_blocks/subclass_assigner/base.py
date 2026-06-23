"""Base class for subclass assignment strategies."""

from __future__ import annotations

from collections.abc import Generator
from typing import cast
from typing import TYPE_CHECKING

from typing_protocol_intersection import ProtocolIntersection

from dnd.character.blueprint.building_blocks.building_block import BuildingBlock
from dnd.character.blueprint.state import Blueprint
from dnd.character.blueprint.state import BlueprintProtocol
from dnd.character.blueprint.state import HasClasses
from dnd.character.blueprint.state import HasSubclasses
from dnd.character.delta.delta import Delta
from dnd.choices.class_creation.character_class import AnySubclass
from dnd.choices.class_creation.character_class import Class
from dnd.choices.class_creation.character_class import subclass_level
from dnd.choices.class_creation.character_class import SUBCLASSES
from pydantic import ConfigDict
from pydantic import Field


class CanNotAssign(ValueError):
    pass


class SubclassDelta(Delta):
    """Delta produced when SubclassAssigner assigns a subclass."""

    subclasses: tuple[AnySubclass, ...]

    def apply[T: BlueprintProtocol](
        self, state: T
    ) -> ProtocolIntersection[T, HasSubclasses]:

        if TYPE_CHECKING:

            class BlueprintWithSubclasses(Blueprint):
                subclasses: tuple[AnySubclass, ...]

        else:

            class BlueprintWithSubclasses(type(state)):
                subclasses: tuple[AnySubclass, ...]

        return cast(
            ProtocolIntersection[T, HasSubclasses],
            BlueprintWithSubclasses.model_validate(
                {**dict(state), "subclasses": self.subclasses}
            ),
        )


def _check_can_assign(class_: Class, state: HasClasses) -> None:
    current_level = state.classes.get_level(class_)
    if current_level == 0:
        raise CanNotAssign(
            f"Cannot assign {class_.value} subclass: "
            f"character does not have {class_.value} class"
        )
    required_level = subclass_level[class_]
    if current_level < required_level:
        raise CanNotAssign(
            f"Cannot assign {class_.value} subclass: "
            f"character level {current_level} "
            f"is below required level {required_level}"
        )


class SubclassAssigner[T: ProtocolIntersection[HasClasses, HasSubclasses]](
    BuildingBlock[T, SubclassDelta, HasSubclasses]
):
    """Base class for assigning a specific subclass to a character.

    Concrete subclasses narrow `class_` to a `Literal[Class.X]` default and
    `subclass` to a `Literal[XxxSubclass.A, ...]` — no method override needed.
    """

    model_config = ConfigDict(frozen=True)

    class_: Class = Field(
        description="The character class for which to assign a subclass"
    )
    subclass: AnySubclass = Field(description="The subclass to assign")

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
        delta = SubclassDelta(subclasses=state.subclasses + (self.subclass,))
        yield delta
        return delta.apply(state)
