"""Base class for subclass assignment strategies."""

from dnd.character.blueprint.building_blocks.building_block import BuildingBlock
from dnd.character.blueprint.states.state import _BPT
from dnd.choices.class_creation.character_class import AnySubclass
from dnd.choices.class_creation.character_class import Class
from dnd.choices.class_creation.character_class import subclass_level
from dnd.choices.class_creation.character_class import SUBCLASSES
from dnd.character.class_levels import ClassLevels
from pydantic import ConfigDict
from pydantic import Field


class CanNotAssign(ValueError):
    pass


def _check_can_assign(class_: Class, classes: ClassLevels) -> None:
    current_level = classes.get_level(class_)
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


class SubclassAssigner(BuildingBlock):
    """Base class for assigning a specific subclass to a character.

    Concrete subclasses narrow `class_` to a `Literal[Class.X]` default and
    `subclass` to a `Literal[XxxSubclass.A, ...]` — no method override needed.
    """

    model_config = ConfigDict(frozen=True)

    class_: Class = Field(
        description="The character class for which to assign a subclass"
    )
    subclass: AnySubclass = Field(description="The subclass to assign")

    def apply(self, blueprint: _BPT) -> _BPT:
        _check_can_assign(self.class_, blueprint.classes)
        subclass_enum = SUBCLASSES[self.class_]
        for existing in blueprint.subclasses:
            if isinstance(existing, subclass_enum):
                return blueprint
        return blueprint.model_copy(
            update={"subclasses": blueprint.subclasses + (self.subclass,)}
        )
