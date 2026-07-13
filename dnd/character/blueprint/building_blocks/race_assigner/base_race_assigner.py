from abc import ABC
from abc import abstractmethod
from typing import Literal

from dnd.character.blueprint.building_blocks.building_block import BuildingBlock
from dnd.character.blueprint.sentinels import (
    _ARK,
    _BAK,
    _BDK,
    _CDK,
    _CLK,
    _DRK,
    _FGK,
    _HeK,
    _MOK,
    _PAK,
    _RAK,
    _ROK,
    _SOK,
    _WAK,
    _WZK,
    _SkCK,
)
from dnd.character.blueprint.states.state import Blueprint
from dnd.character.feature.feats import FeatName
from dnd.character.race.race import Race
from dnd.character.race.subrace_stats.subrace_to_stats import _get_subrace_stats
from dnd.character.race.subraces import SubraceName
from dnd.character.stats import Stats
from pydantic import BaseModel
from pydantic import Field


class RaceSubracePair(BaseModel):
    """A validated pair of race and subrace for internal use by BaseRaceAssigner."""

    race: Race = Field(description="The character's primary race")
    subrace: SubraceName = Field(
        description="The subrace, must be valid for the selected race"
    )


class BaseRaceAssigner(BuildingBlock, ABC):
    """Abstract base for assigning race and subrace to a character."""

    @abstractmethod
    def _get_race_and_subrace(self) -> RaceSubracePair: ...

    def apply(
        self,
        blueprint: Blueprint[
            None,
            Stats,
            _HeK,
            Literal[0],
            _SkCK,
            _WZK,
            _SOK,
            _FGK,
            _BAK,
            _ROK,
            _CLK,
            _DRK,
            _PAK,
            _RAK,
            _MOK,
            _BDK,
            _WAK,
            _ARK,
            _CDK,
        ],
    ) -> Blueprint[
        Race,
        Stats,
        _HeK,
        int,
        int,
        _WZK,
        _SOK,
        _FGK,
        _BAK,
        _ROK,
        _CLK,
        _DRK,
        _PAK,
        _RAK,
        _MOK,
        _BDK,
        _WAK,
        _ARK,
        _CDK,
    ]:
        race_and_subrace = self._get_race_and_subrace()
        subrace_stats = _get_subrace_stats(race_and_subrace.subrace)
        new_stats = Stats(
            strength=blueprint.stats.strength + subrace_stats.statistics.strength,
            dexterity=blueprint.stats.dexterity + subrace_stats.statistics.dexterity,
            constitution=blueprint.stats.constitution
            + subrace_stats.statistics.constitution,
            intelligence=blueprint.stats.intelligence
            + subrace_stats.statistics.intelligence,
            wisdom=blueprint.stats.wisdom + subrace_stats.statistics.wisdom,
            charisma=blueprint.stats.charisma + subrace_stats.statistics.charisma,
        )
        return Blueprint[
            Race,
            Stats,
            _HeK,
            int,
            int,
            _WZK,
            _SOK,
            _FGK,
            _BAK,
            _ROK,
            _CLK,
            _DRK,
            _PAK,
            _RAK,
            _MOK,
            _BDK,
            _WAK,
            _ARK,
            _CDK,
        ].model_validate(
            dict(blueprint)
            | {
                "race": race_and_subrace.race,
                "subrace": race_and_subrace.subrace,
                "speed": subrace_stats.speed,
                "dark_vision_range": max(
                    blueprint.dark_vision_range or 0,
                    subrace_stats.dark_vision_range,
                ),
                "stats": new_stats,
                "languages": blueprint.languages + subrace_stats.languages,
                "skill_proficiencies": (
                    blueprint.skill_proficiencies + subrace_stats.obligatory_skills
                ),
                "tool_proficiencies": (
                    blueprint.tool_proficiencies + subrace_stats.tool_proficiencies
                ),
                "feats": blueprint.feats
                + subrace_stats.additional_feat
                * (FeatName.ANY_EXCEPT_ABILITY_SCORE_IMPROVEMENT,),
                "n_stat_choices": subrace_stats.statistics.any_of_your_choice,
                "n_skill_choices": subrace_stats.n_skills,
                "skills_to_choose_from": frozenset(subrace_stats.skills_to_choose_from),
                "other_active_abilities": (
                    blueprint.other_active_abilities
                    + subrace_stats.other_active_abilities
                ),
            }
        )
