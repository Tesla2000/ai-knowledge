"""Random subclass assigner for character creation."""

from __future__ import annotations

import random

from dnd.character.blueprint.blueprint import Blueprint
from dnd.character.blueprint.building_blocks.subclass_assigner.base import (
    SubclassAssigner,
)
from dnd.choices.class_creation.character_class import (
    AnySubclass,
)
from pydantic import ConfigDict
from pydantic import Field


class RandomSubclassAssigner(SubclassAssigner):
    """Randomly selects a subclass from available options.

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

    seed: int | None = Field(
        default=None,
        description="Optional seed for reproducible random selection",
    )

    def _select_subclass(self, blueprint: Blueprint) -> AnySubclass:
        """Randomly select a subclass for the character's class.

        Args:
            blueprint: Current character blueprint.

        Returns:
            Randomly selected subclass.
        """
        random.seed(self.seed)

        # Randomly select one
        return random.choice(self.available_subclasses)
