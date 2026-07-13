import random

from dnd.character.blueprint.building_blocks.feat_choice_resolver.base import (
    FeatChoiceResolver,
)
from dnd.character.feature.feats import FeatName
from dnd.character.stats import Stats
from typing import Literal
from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)
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

    type: Literal[BuildingBlockType.RANDOM_FEAT_CHOICE_RESOLVER] = (
        BuildingBlockType.RANDOM_FEAT_CHOICE_RESOLVER
    )

    model_config = ConfigDict(frozen=True)

    seed: int | None = Field(
        default=None,
        description="Optional seed for reproducible random selection",
    )

    def _select_from_available(
        self, available: list[FeatName], stats: Stats, stats_cup: Stats
    ) -> FeatName:
        random.seed(self.seed)
        return random.choice(available)
