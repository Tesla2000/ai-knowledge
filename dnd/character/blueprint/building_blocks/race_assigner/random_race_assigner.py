from __future__ import annotations

import random

from dnd.character.blueprint.building_blocks.race_assigner.base_race_assigner import (
    BaseRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner.base_race_assigner import (
    RaceSubracePair,
)
from dnd.character.race.race import Race
from dnd.character.race.subraces import _get_subraces
from typing import Literal
from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)
from pydantic import Field


class RandomRaceAssigner(BaseRaceAssigner):
    """Building block that randomly assigns a race and subrace to a character."""

    type: Literal[BuildingBlockType.RANDOM_RACE_ASSIGNER] = (
        BuildingBlockType.RANDOM_RACE_ASSIGNER
    )

    seed: int | None = Field(
        default=None,
        description="Optional seed for reproducible random selection",
    )

    def _get_race_and_subrace(self) -> RaceSubracePair:
        random.seed(self.seed)

        race = random.choice(tuple(Race))
        subrace = random.choice(_get_subraces(race))
        return RaceSubracePair(race=race, subrace=subrace)
