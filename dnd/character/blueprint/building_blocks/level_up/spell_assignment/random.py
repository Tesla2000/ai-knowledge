import random
from typing import Literal

from dnd.character.blueprint.building_blocks.level_up.spell_assignment.base import (
    SorcererSpellAssigner,
    WizardSpellAssigner,
)
from dnd.character.blueprint.building_blocks.building_block import _WideBlueprint
from dnd.character.spells import Spell
from dnd.choices.class_creation.character_class import Class
from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)
from pydantic import ConfigDict
from pydantic import Field


def _random_select(
    seed: int | None, count: int, available: list[Spell]
) -> tuple[Spell, ...]:
    random.seed(seed)
    return tuple(random.sample(available, min(count, len(available))))


class WizardRandomSpellAssigner(WizardSpellAssigner):
    """Randomly selects wizard spells from the wizard spell list.

    Provides deterministic randomness when seed is set, useful for
    reproducible character generation.

    Example:
        >>> assigner = WizardRandomSpellAssigner(seed=42)
    """

    type: Literal[BuildingBlockType.WIZARD_RANDOM_SPELL_ASSIGNER] = (
        BuildingBlockType.WIZARD_RANDOM_SPELL_ASSIGNER
    )

    model_config = ConfigDict(frozen=True)

    class_: Literal[Class.WIZARD] = Field(
        default=Class.WIZARD, description="Character class this assigner handles"
    )
    seed: int | None = Field(
        default=None,
        description="Optional seed for reproducible random selection",
    )

    def select_spells(
        self,
        spell_level: int,
        count: int,
        available_spells: list[Spell],
        _state: _WideBlueprint,
    ) -> tuple[Spell, ...]:
        return _random_select(self.seed, count, available_spells)


class SorcererRandomSpellAssigner(SorcererSpellAssigner):
    """Randomly selects sorcerer spells from the sorcerer spell list.

    Provides deterministic randomness when seed is set, useful for
    reproducible character generation.

    Example:
        >>> assigner = SorcererRandomSpellAssigner(seed=42)
    """

    type: Literal[BuildingBlockType.SORCERER_RANDOM_SPELL_ASSIGNER] = (
        BuildingBlockType.SORCERER_RANDOM_SPELL_ASSIGNER
    )

    model_config = ConfigDict(frozen=True)

    class_: Literal[Class.SORCERER] = Field(
        default=Class.SORCERER, description="Character class this assigner handles"
    )
    seed: int | None = Field(
        default=None,
        description="Optional seed for reproducible random selection",
    )

    def select_spells(
        self,
        spell_level: int,
        count: int,
        available_spells: list[Spell],
        _state: _WideBlueprint,
    ) -> tuple[Spell, ...]:
        return _random_select(self.seed, count, available_spells)
