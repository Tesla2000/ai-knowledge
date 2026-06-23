from __future__ import annotations

import random

from typing_protocol_intersection import ProtocolIntersection

from dnd.character.blueprint.building_blocks.feat_choice_resolver.base import (
    FeatChoiceResolver,
)
from dnd.character.blueprint.state import HasClasses
from dnd.character.blueprint.state import HasFeats
from dnd.character.blueprint.state import HasStats
from dnd.character.feature.feats import FeatName
from pydantic import ConfigDict
from pydantic import Field


class RandomFeatChoiceResolver[
    T: ProtocolIntersection[ProtocolIntersection[HasFeats, HasStats], HasClasses]
](FeatChoiceResolver[T]):
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

    def _select_from_available(self, available: list[FeatName], state: T) -> FeatName:
        random.seed(self.seed)
        return random.choice(available)
