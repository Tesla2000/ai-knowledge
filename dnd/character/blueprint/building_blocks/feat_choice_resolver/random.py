from __future__ import annotations

import random

from dnd.character.blueprint.blueprint import Blueprint
from dnd.character.blueprint.building_blocks.feat_choice_resolver.base import (
    FeatChoiceResolver,
)
from dnd.character.feature.feats import FeatName
from pydantic import ConfigDict
from pydantic import Field


class RandomFeatChoiceResolver(FeatChoiceResolver):
    """Randomly selects feats for ANY_OF_YOUR_CHOICE placeholders.

    Provides deterministic randomness when seed is set, useful for
    reproducible character generation.

    Example:
        >>> resolver = RandomFeatChoiceResolver(seed=42)
        >>> # or
        >>> resolver = RandomFeatChoiceResolver()  # Truly random
    """

    model_config = ConfigDict(frozen=True)

    seed: int | None = Field(
        default=None,
        description="Optional seed for reproducible random selection",
    )

    def select_from_available(
        self, available: list[FeatName], _: Blueprint
    ) -> FeatName:
        """Randomly select a feat from available options.

        Args:
            available: List of FeatName options to choose from.
            blueprint: Current character blueprint (unused in random selection).

        Returns:
            Randomly selected FeatName.
        """
        random.seed(self.seed)

        return random.choice(available)
