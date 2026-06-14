from __future__ import annotations

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


class SubRaceTemplate(BaseModel):
    name: str
    speed: int
    darkvision_range: int
    languages: list[Language] = Field(
        description="List of languages known by this race"
    )
    obligatory_skills: list[Skill] = Field(
        description="A list of skills always provided by race.",
        default_factory=list,
    )
    skills_to_choose_from: list[Skill] = Field(
        description="A list of skills from which skills can be chosen.",
        default_factory=list,
    )
    n_skills: int = Field(description="Number of skills to choose", default=0)
    tool_proficiencies: list[ToolProficiency | GamingSet | MusicalInstrument] = Field(
        description="List of tool proficiencies.", default_factory=list
    )
    additional_feat: bool = Field(
        "Does sub-race get a feat 'Feat: You gain one Feat of your choice.'"
    )
    statistics: RaceStatistics = Field(
        description="Statistic given by the race and sub-race"
    )
    other_active_abilities: list[str] = Field(
        description="Something like Relentless Endurance or Trance. In other "
        "words abilities that influence gameplay not boosts to "
        "statistics, alignment nor proficiencies."
    )


class MainRaceTemplate(BaseModel):
    sub_races: list[SubRaceTemplate] = Field(
        description="Sub-races of the main race for example for Elf race the "
        "sub-races would be Pallid elf, Dark and High Elf. For "
        "Human Standard and Variant Human. If none is given for "
        "example for Half Orc list the main class in this case "
        "Half Orc."
    )
