from __future__ import annotations
from typing import Self

from dnd.character.race.subrace_stats.race_statistics import (
    RaceStatistics,
)
from dnd.choices.language import Language
from dnd.other_profficiencies import GamingSet
from dnd.other_profficiencies import MusicalInstrument
from dnd.other_profficiencies import ToolProficiency
from dnd.skill_proficiency import Skill
from pydantic import BaseModel
from pydantic import Field
from pydantic import model_validator
from pydantic import NonNegativeInt
from pydantic import PositiveInt


class Subrace(BaseModel):
    speed: PositiveInt
    dark_vision_range: NonNegativeInt
    languages: tuple[Language, ...] = Field(
        description="List of languages known by this race"
    )
    obligatory_skills: tuple[Skill, ...] = Field(
        description="A list of skills always provided by race.",
        default=(),
    )
    skills_to_choose_from: tuple[Skill, ...] = Field(
        description="A list of skills from which skills can be chosen.",
        default_factory=tuple,
    )
    n_skills: int = Field(description="Number of skills to choose", default=0)
    tool_proficiencies: tuple[ToolProficiency | GamingSet | MusicalInstrument, ...] = (
        Field(description="List of tool proficiencies.", default=())
    )
    additional_feat: bool = Field(
        description="Does sub-race get a feat 'Feat: You gain one Feat of your choice.'",
        default=False,
    )
    statistics: RaceStatistics = Field(
        description="Statistic given by the race and sub-race"
    )
    other_active_abilities: tuple[str, ...] = Field(
        description="Something like Relentless Endurance or Trance. In other "
        "words abilities that influence gameplay not boosts to "
        "statistics, alignment nor proficiencies."
    )

    @model_validator(mode="after")
    def _le_skills_to_choose_than_choices(self) -> Self:
        if self.n_skills > len(self.skills_to_choose_from):
            raise ValueError("More skill choices that skills to choose from")
        return self

    @model_validator(mode="after")
    def _no_choices_when_no_skills_to_choose_from(self) -> Self:
        if not self.n_skills and self.skills_to_choose_from:
            raise ValueError(
                "Skills to choose from present but no skill choices available"
            )
        return self
