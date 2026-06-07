from __future__ import annotations

import random
from typing import Optional

from dnd.character.blueprint.blueprint import Blueprint
from dnd.character.blueprint.building_blocks.tool_proficiency_choice_resolver.base import (
    ToolProficiencyChoiceResolver,
)
from dnd.other_profficiencies import GamingSet
from dnd.other_profficiencies import MusicalInstrument
from dnd.other_profficiencies import ToolProficiency
from pydantic import ConfigDict
from pydantic import Field


class RandomToolProficiencyChoiceResolver(ToolProficiencyChoiceResolver):
    """Randomly selects tool proficiencies for ANY_OF_YOUR_CHOICE placeholders.

    Provides deterministic randomness when seed is set, useful for
    reproducible character generation.

    Example:
        >>> resolver = RandomToolProficiencyChoiceResolver(seed=42)
        >>> # or
        >>> resolver = RandomToolProficiencyChoiceResolver()  # Truly random
    """

    model_config = ConfigDict(frozen=True)

    seed: Optional[int] = Field(
        default=None,
        description="Optional seed for reproducible random selection",
    )

    def _select_tool_proficiency(
        self, available: list[ToolProficiency], _: Blueprint
    ) -> ToolProficiency:
        """Randomly select a tool proficiency from available options.

        Args:
            available: List of ToolProficiency options to choose from.
            blueprint: Current character blueprint (unused in random selection).

        Returns:
            Randomly selected ToolProficiency.
        """
        random.seed(self.seed)

        return random.choice(available)

    def _select_gaming_set(
        self, available: list[GamingSet], _: Blueprint
    ) -> GamingSet:
        """Randomly select a gaming set from available options.

        Args:
            available: List of GamingSet options to choose from.
            blueprint: Current character blueprint (unused in random selection).

        Returns:
            Randomly selected GamingSet.
        """
        random.seed(self.seed)

        return random.choice(available)

    def _select_musical_instrument(
        self, available: list[MusicalInstrument], _: Blueprint
    ) -> MusicalInstrument:
        """Randomly select a musical instrument from available options.

        Args:
            available: List of MusicalInstrument options to choose from.
            blueprint: Current character blueprint (unused in random selection).

        Returns:
            Randomly selected MusicalInstrument.
        """
        random.seed(self.seed)

        return random.choice(available)
