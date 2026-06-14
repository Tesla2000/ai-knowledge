from __future__ import annotations

import random

from dnd.character.blueprint.blueprint import Blueprint
from dnd.character.blueprint.building_blocks.language_choice_resolver.base import (
    LanguageChoiceResolver,
)
from dnd.choices.language import Language
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

    model_config = ConfigDict(frozen=True)

    seed: int | None = Field(
        default=None,
        description="Optional seed for reproducible random selection",
    )

    def _select_from_available(
        self, available: list[Language], _: Blueprint
    ) -> Language:
        """Randomly select a language from available options.

        Args:
            available: List of Language options to choose from.
            blueprint: Current character blueprint (unused in random selection).

        Returns:
            Randomly selected Language.
        """
        random.seed(self.seed)

        return random.choice(available)
