from __future__ import annotations

from typing import NamedTuple

from dnd.character.blueprint.blueprint import Blueprint
from dnd.character.blueprint.building_blocks import (  # type: ignore[attr-defined]
    CombinedBlock,
)
from dnd.character.blueprint.building_blocks.all_choices_resolver import (
    AnyChoiceResolver,
)
from dnd.character.blueprint.building_blocks.level_up.health_increase import (
    AnyHealthIncrease,
)
from dnd.character.blueprint.building_blocks.level_up.level_incrementer import (
    LevelIncrementer,
)
from dnd.character.blueprint.building_blocks.level_up.spell_assignment import (
    AnySpellAssigner,
)
from pydantic import Field


class LevelUpBlocks(NamedTuple):
    level_increment: LevelIncrementer
    health_increase: AnyHealthIncrease
    spell_assigner: AnySpellAssigner
    all_choice_resolver: AnyChoiceResolver


class LevelUp(CombinedBlock):
    """Adds one level to a specific class.

    Increments the level for the specified class by 1. Validates that total
    character level doesn't exceed the blueprint's level field.

    Accepts any implementation of AllChoicesResolverBase, allowing
    flexibility between sequential resolvers (AllChoicesResolver) and
    holistic AI resolvers (AIAllChoicesResolver).

    Example:
        >>> builder = Builder([
        ...     LevelAssigner(level=10),
        ...     LevelUp(class_=Class.FIGHTER),  # +1 level
        ...     LevelUp(class_=Class.FIGHTER),  # +1 level
        ...     LevelUp(class_=Class.WIZARD),   # +1 level
        ... ])  # Character at level 10 with 2 Fighter / 1 Wizard (7 unused levels)
    """

    blocks: LevelUpBlocks = Field(
        description="Level increment, health increase, spell assignment, and choice resolution",
    )

    def _get_change(self, blueprint: Blueprint) -> Blueprint:
        if blueprint.race is None:
            raise ValueError("Race must be chosen before leveling up")
        return super().get_change(blueprint)  # type: ignore[no-any-return,misc]
