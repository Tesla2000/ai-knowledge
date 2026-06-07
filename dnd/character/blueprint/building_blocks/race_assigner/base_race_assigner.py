from abc import ABC
from abc import abstractmethod
from typing import Self

from dnd.character.blueprint.blueprint import Blueprint
from dnd.character.blueprint.building_blocks.building_block import (
    BuildingBlock,
)
from dnd.character.race.race import Race
from dnd.character.race.subrace_stats.subrace_to_stats import (
    SUBRACE_STATS,
)
from dnd.character.race.subraces import RACE_TO_SUBRACES
from dnd.character.race.subraces import Subrace
from pydantic import BaseModel
from pydantic import Field
from pydantic import model_validator


class RaceSubracePair(BaseModel):
    """Represents a valid combination of race and subrace for character creation.

    Ensures that the selected subrace belongs to the selected race through validation.
    """

    race: Race = Field(description="The character's primary race")
    subrace: Subrace = Field(
        description="The subrace, must be valid for the selected race"
    )

    @model_validator(mode="after")
    def _check_subrace_correctness(self) -> Self:
        if self.subrace in RACE_TO_SUBRACES[self.race]:
            return self
        raise ValueError(
            f"Subrace {self.subrace} is not a subrace of {self.race}"
        )


class BaseRaceAssigner(BuildingBlock, ABC):
    @abstractmethod
    def _get_race_and_subrace(self) -> RaceSubracePair:
        pass

    def get_change(self, blueprint: Blueprint) -> Blueprint:
        """Yield the race difference."""
        if blueprint.race is not None:
            raise ValueError(f"{blueprint=} already has a race assigned")
        # TODO: add stat assigners for all classes and subclasses
        race_and_subrace = self._get_race_and_subrace()
        subrace_stats = SUBRACE_STATS[race_and_subrace.subrace].add_to(
            blueprint
        )
        return subrace_stats.model_copy(
            update=Blueprint(
                race=race_and_subrace.race,
                subrace=race_and_subrace.subrace,
            ).model_dump(exclude_unset=True)
        )
