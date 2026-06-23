from __future__ import annotations

import random
from typing import Literal

from dnd.character.blueprint.building_blocks.level_up.spell_assignment.base import (
    SorcererSpellAssigner,
    WizardSpellAssigner,
)
from dnd.character.blueprint.state import HasSorcererLevel
from dnd.character.blueprint.state import HasWizardLevel
from dnd.character.spells import Spell
from dnd.choices.class_creation.character_class import Class
from pydantic import ConfigDict
from pydantic import Field


def _random_select(
    seed: int | None, count: int, available: list[Spell]
) -> tuple[Spell, ...]:
    random.seed(seed)
    return tuple(random.sample(available, min(count, len(available))))


class WizardRandomSpellAssigner[T: HasWizardLevel](WizardSpellAssigner[T]):
    """Randomly selects wizard spells from the wizard spell list.

    Provides deterministic randomness when seed is set, useful for
    reproducible character generation.

    Example:
        >>> assigner = WizardRandomSpellAssigner(seed=42)
    """

    model_config = ConfigDict(frozen=True)

    class_: Literal[Class.WIZARD] = Field(
        default=Class.WIZARD, description="Character class this assigner handles"
    )
    seed: int | None = Field(
        default=None,
        description="Optional seed for reproducible random selection",
    )

    def _select_spells(
        self,
        spell_level: int,
        count: int,
        available_spells: list[Spell],
        _state: T,
    ) -> tuple[Spell, ...]:
        return _random_select(self.seed, count, available_spells)


class SorcererRandomSpellAssigner[T: HasSorcererLevel](SorcererSpellAssigner[T]):
    """Randomly selects sorcerer spells from the sorcerer spell list.

    Provides deterministic randomness when seed is set, useful for
    reproducible character generation.

    Example:
        >>> assigner = SorcererRandomSpellAssigner(seed=42)
    """

    model_config = ConfigDict(frozen=True)

    class_: Literal[Class.SORCERER] = Field(
        default=Class.SORCERER, description="Character class this assigner handles"
    )
    seed: int | None = Field(
        default=None,
        description="Optional seed for reproducible random selection",
    )

    def _select_spells(
        self,
        spell_level: int,
        count: int,
        available_spells: list[Spell],
        _state: T,
    ) -> tuple[Spell, ...]:
        return _random_select(self.seed, count, available_spells)
