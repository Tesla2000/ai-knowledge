from __future__ import annotations

from collections.abc import Generator
from typing import NamedTuple
from typing import Never
from typing import overload

from typing_extensions import deprecated

from dnd.character.blueprint.building_blocks import (
    CombinedBlock,
)
from dnd.character.blueprint.state import Blueprint
from dnd.character.blueprint.state import BlueprintProtocol
from dnd.character.blueprint.state import HasRace
from dnd.character.blueprint.building_blocks.all_choices_resolver import (
    AnyChoiceResolver,
)
from dnd.character.blueprint.building_blocks.level_up.health_increase import (
    AnyHealthIncrease,
)
from dnd.character.blueprint.building_blocks.level_up.level_incrementer import (
    SorcererLevelIncrementer,
    WizardLevelIncrementer,
)
from dnd.character.blueprint.building_blocks.level_up.spell_assignment import (
    AnySpellAssigner,
)
from dnd.character.delta.delta import Delta
from pydantic import Field


class LevelUpBlocks(NamedTuple):
    level_increment: WizardLevelIncrementer | SorcererLevelIncrementer
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

    @overload
    @deprecated("Race must be chosen before leveling up")
    def get_change(self, state: Blueprint) -> Never: ...

    @overload
    def get_change(
        self, state: HasRace
    ) -> Generator[Delta, None, BlueprintProtocol]: ...

    @overload
    def get_change(
        self, state: BlueprintProtocol
    ) -> Generator[Delta, None, BlueprintProtocol]: ...

    def get_change(
        self, state: BlueprintProtocol
    ) -> Generator[Delta, None, BlueprintProtocol]:
        if not isinstance(state, HasRace):
            raise ValueError("Race must be chosen before leveling up")
        return (yield from super().get_change(state))
