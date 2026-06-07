import random
from typing import Optional

from dnd.character.blueprint.building_blocks.race_assigner.base_race_assigner import (
    BaseRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner.base_race_assigner import (
    RaceSubracePair,
)
from dnd.character.race.race import Race
from dnd.character.race.subraces import RACE_TO_SUBRACES
from pydantic import Field


class RandomRaceAssigner(BaseRaceAssigner):
    """Building block that randomly assigns a race and subrace to a character."""

    seed: Optional[int] = Field(
        default=None,
        description="Optional seed for reproducible random selection",
    )

    def _get_race_and_subrace(self) -> RaceSubracePair:
        random.seed(self.seed)

        race = random.choice(tuple(Race))
        subrace = random.choice(RACE_TO_SUBRACES[race])
        return RaceSubracePair(race=race, subrace=subrace)
