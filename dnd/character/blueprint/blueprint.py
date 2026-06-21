from __future__ import annotations

from typing import Self

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

type Equipment = WeaponName | ArmorName | str


class Blueprint(Character):
    """Blueprint for building a Character with optional fields.

    All required fields from Character are optional in Blueprint, allowing
    incremental character construction through building blocks.
    """

    # Override required fields to be optional
    sex: Sex | None = None  # type: ignore[assignment]
    backstory: str | None = None  # type: ignore[assignment]
    level: ClassLevel | None = None  # type: ignore[assignment]
    age: PositiveInt | None = None  # type: ignore[assignment]
    race: Race | None = None  # type: ignore[assignment]
    subrace: Subrace | None = None  # type: ignore[assignment]
    name: str | None = None  # type: ignore[assignment]
    background: Background | None = None  # type: ignore[assignment]
    alignment: Alignment | None = None  # type: ignore[assignment]
    height: PositiveInt | None = None  # type: ignore[assignment]
    weight: PositiveInt | None = None  # type: ignore[assignment]
    eye_color: str | None = None  # type: ignore[assignment]
    skin_color: str | None = None  # type: ignore[assignment]
    hairstyle: str | None = None  # type: ignore[assignment]
    appearance: str | None = None  # type: ignore[assignment]
    character_traits: str | None = None  # type: ignore[assignment]
    ideals: str | None = None  # type: ignore[assignment]
    bonds: str | None = None  # type: ignore[assignment]
    weaknesses: str | None = None  # type: ignore[assignment]

    stats: Stats | None = None  # type: ignore[assignment]
    health_base: PositiveInt | None = None  # type: ignore[assignment]
    dark_vision_range: NonNegativeInt | None = None  # type: ignore[assignment]
    speed: PositiveInt | None = None  # type: ignore[assignment]
    n_stat_choices: NonNegativeInt = 0
    n_skill_choices: NonNegativeInt = 0
    skills_to_choose_from: frozenset[Skill] = Field(
        default_factory=frozenset,
        description="Skills from which n_skill_choices can be chosen",
    )
    languages: tuple[Language, ...] = Field(default=())  # type: ignore[assignment]
    skill_proficiencies: tuple[Skill, ...] = Field(  # type: ignore[assignment]
        default=(), description="Skills the character is proficient in"
    )
    feats: tuple[FeatName, ...] = Field(  # type: ignore[assignment]
        description="Feats from a list fitting description of the character if"
        " race is variant human at least one must be different "
        "than ability score improvement",
        default=(),
    )
    tool_proficiencies: tuple[ToolProficiency | GamingSet | MusicalInstrument, ...] = (
        Field(default=(), description="Tool proficiencies")  # type: ignore[assignment]
    )
    saving_throw_proficiencies: tuple[Statistic, ...] = ()
    equipment_choices: tuple[tuple[Equipment, ...], ...] = ()
    other_active_abilities: tuple[str, ...] = ()
    ac_bonus: NonNegativeInt = 0
    spell_save_dc_bonus: NonNegativeInt = 0
    spellcasting_ability_bonus: NonNegativeInt = 0

    def add_diff(self, diff: Self) -> Self:
        return self.model_copy(
            update={
                field_name: field_value
                for field_name, field_value in diff
                if field_name in diff.model_fields_set
            }
        )
