import random

from dnd.character.blueprint.building_blocks.language_choice_resolver.base import (
    LanguageChoiceResolver,
)
from dnd.choices.language import Language
from typing import Literal
from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)
from pydantic import ConfigDict
from pydantic import Field


class RandomLanguageChoiceResolver(LanguageChoiceResolver):
    """Randomly selects languages for ANY_OF_YOUR_CHOICE placeholders.

    Provides deterministic randomness when seed is set, useful for
    reproducible character generation.

    Example:
        >>> resolver = RandomLanguageChoiceResolver(seed=42)
        >>> # or
        >>> resolver = RandomLanguageChoiceResolver()  # Truly random
    """

    type: Literal[BuildingBlockType.RANDOM_LANGUAGE_CHOICE_RESOLVER] = (
        BuildingBlockType.RANDOM_LANGUAGE_CHOICE_RESOLVER
    )

    model_config = ConfigDict(frozen=True)

    seed: int | None = Field(
        default=None,
        description="Optional seed for reproducible random selection",
    )

    def _select_from_available(
        self, available: list[Language], languages: tuple[Language, ...]
    ) -> Language:
        random.seed(self.seed)
        return random.choice(available)
