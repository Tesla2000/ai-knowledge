"""Base class for subclass assignment strategies."""

from __future__ import annotations


from abc import ABC
from abc import abstractmethod

from dnd.character.blueprint.blueprint import Blueprint
from dnd.character.blueprint.building_blocks.building_block import (
    BuildingBlock,
)
from dnd.choices.class_creation.character_class import (
    AnySubclass,
)
from dnd.choices.class_creation.character_class import Class
from dnd.choices.class_creation.character_class import (
    subclass_level,
)
from dnd.choices.class_creation.character_class import (
    SUBCLASSES,
)
from pydantic import ConfigDict
from pydantic import Field
from pydantic import model_validator


class CanNotAssign(ValueError):
    pass


class SubclassAssigner(BuildingBlock, ABC):
    """Abstract base class for assigning subclasses to characters.

    Subclasses must implement _select_subclass to determine which subclass
    to assign based on the character's class and context.

    Example:
        >>> from dnd.choices.class_creation.character_class import Class
        >>> assigner = SomeSubclassAssigner(class_=Class.WIZARD)
        >>> builder = Builder().add(assigner)
    """

    model_config = ConfigDict(frozen=True)

    class_: Class = Field(
        description="The character class for which to assign a subclass"
    )
    available_subclasses: tuple[AnySubclass, ...] = Field(
        default=None,  # type: ignore[arg-type]
        description="Tuple of subclasses available for selection (defaults to all valid subclasses)",
    )

    @model_validator(mode="before")
    @classmethod
    def _add_available_subclasses(
        cls,
        data: dict[str, object],  # ignore
    ) -> dict[str, object]:  # ignore
        class_ = Class(data.get("class_"))  # type: ignore[arg-type]
        subclass_enum = SUBCLASSES[class_]
        available_subclasses = data.get("available_subclasses", tuple(subclass_enum))
        if any(subclass not in subclass_enum for subclass in available_subclasses):  # type: ignore[attr-defined]
            raise ValueError(
                f"Not all subclasses of {available_subclasses} are available to {class_}"
            )
        data["available_subclasses"] = available_subclasses
        return data

    @abstractmethod
    def _select_subclass(self, blueprint: Blueprint) -> AnySubclass:
        """Select a subclass for the character's class.

        Args:
            blueprint: Current character blueprint containing:
                - classes: The character's classes and levels
                - Other character context for informed selection

        Returns:
            Selected subclass appropriate for the character's class.
        """

    def get_change(self, blueprint: Blueprint) -> Blueprint:
        """Assign a subclass to the character.

        Args:
            blueprint: Current character blueprint.

        Returns:
            Blueprint with subclass added.

        Raises:
            CanNotAssign: If class is not in character's classes or level is too low.
        """
        # Validate class exists in character
        if self.class_ not in blueprint.classes:
            raise CanNotAssign(
                f"Cannot assign {self.class_.value} subclass: "
                f"character does not have {self.class_.value} class"
            )

        # Check if character level is high enough for subclass
        required_level = subclass_level[self.class_]
        if blueprint.classes[self.class_] < required_level:
            raise CanNotAssign(
                f"Cannot assign {self.class_.value} subclass: "
                f"character level {blueprint.classes[self.class_]} "
                f"is below required level {required_level}"
            )

        # Check if character already has a subclass for this class
        subclass_enum = SUBCLASSES[self.class_]
        existing_subclass = None
        for existing in blueprint.subclasses:
            if isinstance(existing, subclass_enum):
                existing_subclass = existing
                break

        if existing_subclass:
            # Already has a subclass for this class
            return Blueprint()

        # Select subclass
        selected_subclass = self._select_subclass(blueprint)

        # Validate selected subclass matches class
        if not isinstance(selected_subclass, subclass_enum):
            raise ValueError(
                f"Selected subclass {selected_subclass} "
                f"is not valid for {self.class_.value}"
            )

        # Add subclass to character
        new_subclasses = blueprint.subclasses + (selected_subclass,)

        return Blueprint(subclasses=new_subclasses)
