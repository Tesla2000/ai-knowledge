from __future__ import annotations

import random

from dnd.character.blueprint.blueprint import Blueprint
from dnd.character.blueprint.building_blocks.level_up.spell_assignment.base import (
    SpellAssigner,
)
from dnd.character.spells import Spell
from pydantic import ConfigDict
from pydantic import Field


class RandomSpellAssigner(SpellAssigner):
    """Randomly selects spells from available class spell list.

    Provides deterministic randomness when seed is set, useful for
    reproducible character generation.

    Example:
        >>> assigner = RandomSpellAssigner(
        ...     class_=Class.WIZARD,
        ...     seed=42,  # Reproducible
        ... )
    """

    model_config = ConfigDict(frozen=True)

    seed: int | None = Field(
        default=None,
        description="Optional seed for reproducible random selection",
    )

    def _select_spells(
        self,
        spell_level: int,
        count: int,
        available_spells: list[Spell],
        blueprint: Blueprint,
    ) -> tuple[Spell, ...]:
        """Randomly select N unique spells from available list.

        Args:
            spell_level: The spell level (0-9).
            count: Number of spells to select.
            available_spells: Filtered list of available spells.
            blueprint: Current character blueprint (unused for random).

        Returns:
            Tuple of randomly selected spells.
        """
        # Set random seed if provided (for reproducibility)
        random.seed(self.seed)

        # Random selection - take min of count and available
        n = min(count, len(available_spells))
        return tuple(random.sample(available_spells, n))
