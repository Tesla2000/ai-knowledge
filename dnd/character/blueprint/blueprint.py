from __future__ import annotations

from typing import Self
from typing import Union

from dnd.character.armor.names import ArmorName
from dnd.character.character import Character
from dnd.character.character import ClassLevel
from dnd.character.feature.feats import FeatName
from dnd.character.race.race import Race
from dnd.character.race.subraces import Subrace
from dnd.character.stats import Stats
from dnd.choices.alignment import Alignment
from dnd.choices.background_creatrion.background import (
    Background,
)
from dnd.choices.equipment_creation.weapons import WeaponName
from dnd.choices.language import Language
from dnd.choices.sex import Sex
from dnd.choices.stats_creation.statistic import Statistic
from dnd.other_profficiencies import GamingSet
from dnd.other_profficiencies import MusicalInstrument
from dnd.other_profficiencies import ToolProficiency
from dnd.skill_proficiency import Skill
from pydantic import Field
from pydantic import NonNegativeInt
from pydantic import PositiveInt

Equipment = Union[WeaponName, ArmorName, str]


class Blueprint(Character):
    """Blueprint for building a Character with optional fields.

    All required fields from Character are optional in Blueprint, allowing
    incremental character construction through building blocks.
    """

    # Override required fields to be optional
    sex: Sex | None = None
    backstory: str | None = None
    level: ClassLevel | None = None
    age: PositiveInt | None = None
    race: Race | None = None
    subrace: Subrace | None = None
    name: str | None = None
    background: Background | None = None
    alignment: Alignment | None = None
    height: PositiveInt | None = None
    weight: PositiveInt | None = None
    eye_color: str | None = None
    skin_color: str | None = None
    hairstyle: str | None = None
    appearance: str | None = None
    character_traits: str | None = None
    ideals: str | None = None
    bonds: str | None = None
    weaknesses: str | None = None

    stats: Stats | None = None
    health_base: PositiveInt | None = None
    dark_vision_range: NonNegativeInt | None = None
    speed: PositiveInt | None = None
    n_stat_choices: NonNegativeInt = 0
    n_skill_choices: NonNegativeInt = 0
    skills_to_choose_from: frozenset[Skill] = Field(
        default_factory=frozenset,
        description="Skills from which n_skill_choices can be chosen",
    )
    languages: tuple[Language, ...] = Field(default=())
    skill_proficiencies: tuple[Skill, ...] = Field(
        default=(), description="Skills the character is proficient in"
    )
    feats: tuple[FeatName, ...] = Field(
        description="Feats from a list fitting description of the character if"
        " race is variant human at least one must be different "
        "than ability score improvement",
        default=(),
    )
    tool_proficiencies: tuple[ToolProficiency | GamingSet | MusicalInstrument, ...] = (
        Field(default=(), description="Tool proficiencies")
    )
    saving_throw_proficiencies: tuple[Statistic, ...] = ()
    equipment_choices: tuple[tuple[Equipment, ...], ...] = ()
    other_active_abilities: tuple[str, ...] = ()

    def add_diff(self, diff: Self) -> Self:
        return self.model_copy(
            update={
                field_name: field_value
                for field_name, field_value in diff
                if field_name in diff.model_fields_set
            }
        )
