from __future__ import annotations

from typing import Self

from dnd.character.blueprint.blueprint import Blueprint
from dnd.character.feature.feats import FeatName
from dnd.character.race.subrace_stats.race_statistics import (
    RaceStatistics,
)
from dnd.character.stats import Stats
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


class SubraceStats(BaseModel):
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
    additional_feat: bool = Field(  # type: ignore[assignment]
        "Does sub-race get a feat 'Feat: You gain one Feat of your choice.'"
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

    def add_to(self, blueprint: Blueprint) -> Blueprint:
        """Apply subrace statistics to the blueprint.

        Updates blueprint with subrace-specific values including speed,
        dark vision, languages, skill proficiencies, tool proficiencies,
        and ability score bonuses from race/subrace.
        """
        if not blueprint.stats:
            raise ValueError("Stats must be set before race can be assigned")
        new_stats = Stats(
            strength=blueprint.stats.strength + self.statistics.strength,
            dexterity=blueprint.stats.dexterity + self.statistics.dexterity,
            constitution=blueprint.stats.constitution + self.statistics.constitution,
            intelligence=blueprint.stats.intelligence + self.statistics.intelligence,
            wisdom=blueprint.stats.wisdom + self.statistics.wisdom,
            charisma=blueprint.stats.charisma + self.statistics.charisma,
        )

        return Blueprint(
            speed=self.speed,
            dark_vision_range=max(
                blueprint.dark_vision_range or 0, self.dark_vision_range
            ),
            languages=blueprint.languages + self.languages,
            skill_proficiencies=blueprint.skill_proficiencies + self.obligatory_skills,
            tool_proficiencies=blueprint.tool_proficiencies + self.tool_proficiencies,
            stats=new_stats,
            feats=blueprint.feats
            + self.additional_feat * (FeatName.ANY_EXCEPT_ABILITY_SCORE_IMPROVEMENT,),
            n_stat_choices=self.statistics.any_of_your_choice,
            n_skill_choices=self.n_skills,
            skills_to_choose_from=frozenset(self.skills_to_choose_from),
            other_active_abilities=self.other_active_abilities,
        )
