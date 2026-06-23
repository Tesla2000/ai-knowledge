from __future__ import annotations

import random

from dnd.character.blueprint.building_blocks.tool_proficiency_choice_resolver.base import (
    ToolProficiencyChoiceResolver,
)
from dnd.character.blueprint.state import HasToolProficiencies
from dnd.other_profficiencies import GamingSet
from dnd.other_profficiencies import MusicalInstrument
from dnd.other_profficiencies import ToolProficiency
from pydantic import ConfigDict
from pydantic import Field


class RandomToolProficiencyChoiceResolver[T: HasToolProficiencies](
    ToolProficiencyChoiceResolver[T]
):
    """Randomly selects tool proficiencies for ANY_OF_YOUR_CHOICE placeholders.

    Provides deterministic randomness when seed is set, useful for
    reproducible character generation.

    Example:
        >>> resolver = RandomToolProficiencyChoiceResolver(seed=42)
        >>> # or
        >>> resolver = RandomToolProficiencyChoiceResolver()  # Truly random
    """

    model_config = ConfigDict(frozen=True)

    seed: int | None = Field(
        default=None,
        description="Optional seed for reproducible random selection",
    )

    def _select_tool_proficiency(
        self, available: list[ToolProficiency], state: T
    ) -> ToolProficiency:
        random.seed(self.seed)
        return random.choice(available)

    def _select_gaming_set(self, available: list[GamingSet], state: T) -> GamingSet:
        random.seed(self.seed)
        return random.choice(available)

    def _select_musical_instrument(
        self, available: list[MusicalInstrument], state: T
    ) -> MusicalInstrument:
        random.seed(self.seed)
        return random.choice(available)
