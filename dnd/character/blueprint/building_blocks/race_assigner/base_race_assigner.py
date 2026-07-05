from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from collections.abc import Generator
from typing import cast
from typing import Never
from typing import overload
from typing import TYPE_CHECKING

from typing_extensions import deprecated

from typing_protocol_intersection import ProtocolIntersection

from dnd.character.blueprint.building_blocks.building_block import BuildingBlock
from dnd.character.blueprint.state import Blueprint
from dnd.character.blueprint.state import BlueprintProtocol
from dnd.character.blueprint.state import HasFeats
from dnd.character.blueprint.state import HasLanguages
from dnd.character.blueprint.state import HasRace
from dnd.character.blueprint.state import HasSkillProficiencies
from dnd.character.blueprint.state import HasStats
from dnd.character.blueprint.state import HasToolProficiencies
from dnd.character.delta.delta import Delta
from dnd.character.feature.feats import FeatName
from dnd.character.race.race import Race
from dnd.character.race.subrace_stats.subrace_to_stats import _get_subrace_stats
from dnd.character.race.subraces import SubraceName
from dnd.character.stats import Stats
from dnd.choices.language import Language
from dnd.other_profficiencies import GamingSet
from dnd.other_profficiencies import MusicalInstrument
from dnd.other_profficiencies import ToolProficiency
from dnd.skill_proficiency import Skill
from pydantic import BaseModel
from pydantic import Field
from pydantic import NonNegativeInt
from pydantic import PositiveInt


class RaceSubracePair(BaseModel):
    """A validated pair of race and subrace for internal use by BaseRaceAssigner."""

    race: Race = Field(description="The character's primary race")
    subrace: SubraceName = Field(
        description="The subrace, must be valid for the selected race"
    )


class RaceDelta(Delta):
    """Delta produced when BaseRaceAssigner sets the character race and applies subrace stats."""

    race: Race
    subrace: SubraceName
    speed: PositiveInt
    dark_vision_range: NonNegativeInt
    stats: Stats
    languages: tuple[Language, ...]
    skill_proficiencies: tuple[Skill, ...]
    tool_proficiencies: tuple[ToolProficiency | GamingSet | MusicalInstrument, ...]
    feats: tuple[FeatName, ...]
    n_stat_choices: int
    n_skill_choices: int
    skills_to_choose_from: frozenset[Skill]
    other_active_abilities: tuple[str, ...]

    def apply[T: BlueprintProtocol](self, state: T) -> ProtocolIntersection[T, HasRace]:
        if TYPE_CHECKING:

            class BlueprintWithRace(Blueprint):
                race: Race
                subrace: SubraceName
                speed: PositiveInt
                dark_vision_range: NonNegativeInt
                stats: Stats
                languages: tuple[Language, ...]
                skill_proficiencies: tuple[Skill, ...]
                tool_proficiencies: tuple[
                    ToolProficiency | GamingSet | MusicalInstrument, ...
                ]
                feats: tuple[FeatName, ...]
                n_stat_choices: int
                n_skill_choices: int
                skills_to_choose_from: frozenset[Skill]
                other_active_abilities: tuple[str, ...]

        else:

            class BlueprintWithRace(type(state)):
                race: Race
                subrace: SubraceName
                speed: PositiveInt
                dark_vision_range: NonNegativeInt
                stats: Stats
                languages: tuple[Language, ...]
                skill_proficiencies: tuple[Skill, ...]
                tool_proficiencies: tuple[
                    ToolProficiency | GamingSet | MusicalInstrument, ...
                ]
                feats: tuple[FeatName, ...]
                n_stat_choices: int
                n_skill_choices: int
                skills_to_choose_from: frozenset[Skill]
                other_active_abilities: tuple[str, ...]

        return cast(
            ProtocolIntersection[T, HasRace],
            BlueprintWithRace.model_validate(
                dict(state)
                | {
                    "race": self.race,
                    "subrace": self.subrace,
                    "speed": self.speed,
                    "dark_vision_range": self.dark_vision_range,
                    "stats": self.stats,
                    "languages": self.languages,
                    "skill_proficiencies": self.skill_proficiencies,
                    "tool_proficiencies": self.tool_proficiencies,
                    "feats": self.feats,
                    "n_stat_choices": self.n_stat_choices,
                    "n_skill_choices": self.n_skill_choices,
                    "skills_to_choose_from": self.skills_to_choose_from,
                    "other_active_abilities": self.other_active_abilities,
                }
            ),
        )


class BaseRaceAssigner[T: HasStats](BuildingBlock[T, RaceDelta, HasRace], ABC):
    """Abstract base for assigning race and subrace to a character."""

    @abstractmethod
    def _get_race_and_subrace(self) -> RaceSubracePair: ...

    @overload
    @deprecated("Cannot assign race to a state that already has a race assigned")
    def get_change(self, state: HasRace) -> Never: ...

    @overload
    def get_change(
        self, state: T
    ) -> Generator[RaceDelta, None, ProtocolIntersection[T, HasRace]]: ...

    def get_change(
        self, state: T | HasRace
    ) -> Generator[RaceDelta, None, ProtocolIntersection[T, HasRace]]:
        if isinstance(state, HasRace):
            raise ValueError(f"{state} already has a race assigned")

        race_and_subrace = self._get_race_and_subrace()
        subrace_stats = _get_subrace_stats(race_and_subrace.subrace)

        new_stats = Stats(
            strength=state.stats.strength + subrace_stats.statistics.strength,
            dexterity=state.stats.dexterity + subrace_stats.statistics.dexterity,
            constitution=state.stats.constitution
            + subrace_stats.statistics.constitution,
            intelligence=state.stats.intelligence
            + subrace_stats.statistics.intelligence,
            wisdom=state.stats.wisdom + subrace_stats.statistics.wisdom,
            charisma=state.stats.charisma + subrace_stats.statistics.charisma,
        )

        delta = RaceDelta(
            race=race_and_subrace.race,
            subrace=race_and_subrace.subrace,
            speed=subrace_stats.speed,
            dark_vision_range=max(
                state.dark_vision_range if isinstance(state, HasRace) else 0,
                subrace_stats.dark_vision_range,
            ),
            stats=new_stats,
            languages=(state.languages if isinstance(state, HasLanguages) else ())
            + subrace_stats.languages,
            skill_proficiencies=(
                state.skill_proficiencies
                if isinstance(state, HasSkillProficiencies)
                else ()
            )
            + subrace_stats.obligatory_skills,
            tool_proficiencies=(
                state.tool_proficiencies
                if isinstance(state, HasToolProficiencies)
                else ()
            )
            + subrace_stats.tool_proficiencies,
            feats=(state.feats if isinstance(state, HasFeats) else ())
            + subrace_stats.additional_feat
            * (FeatName.ANY_EXCEPT_ABILITY_SCORE_IMPROVEMENT,),
            n_stat_choices=subrace_stats.statistics.any_of_your_choice,
            n_skill_choices=subrace_stats.n_skills,
            skills_to_choose_from=frozenset(subrace_stats.skills_to_choose_from),
            other_active_abilities=subrace_stats.other_active_abilities,
        )
        yield delta
        return delta.apply(state)
