from __future__ import annotations

from dnd.character.blueprint.building_blocks.race_assigner.base_race_assigner import (
    BaseRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner.base_race_assigner import (
    RaceSubracePair,
)
from dnd.character.race.race import Race
from dnd.character.race.subraces import Subrace
from pydantic import Field


class RaceAssigner(BaseRaceAssigner):
    """Assigns a race to the character."""

    race: Race = Field(description="Character's race selection")
    subrace: Subrace = Field(description="Character's subrace selection")

    def _get_race_and_subrace(self) -> RaceSubracePair:
        return RaceSubracePair(race=self.race, subrace=self.subrace)
