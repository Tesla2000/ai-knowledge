from __future__ import annotations

from itertools import filterfalse
from typing import Any
from typing import Optional
from typing import TYPE_CHECKING

from dnd.character.ability import Ability
from dnd.choices.stats_creation.statistic import (
    StatisticAndAny,
)
from dnd.other_profficiencies import ArmorProficiency
from dnd.other_profficiencies import GamingSet
from dnd.other_profficiencies import MusicalInstrument
from dnd.other_profficiencies import ToolProficiency
from dnd.other_profficiencies import WeaponProficiency
from dnd.skill_proficiency import Skill
from pydantic import BaseModel
from pydantic import Field


if TYPE_CHECKING:
    from dnd.character.blueprint.blueprint import Blueprint


class Feature(BaseModel):
    source: Optional[str]
    ability: Optional[Ability]
    skill_proficiency_gain: Optional[Skill]
    skill_expertise_gain: Optional[Skill] = Field(
        description="The same as double proficiency."
    )
    tool_proficiency_gain: Optional[ToolProficiency]
    instrument_proficiency_gain: Optional[MusicalInstrument]
    gaming_set_proficiency_gain: Optional[GamingSet]
    weapon_proficiencies_gain: list[WeaponProficiency] = Field(
        description="Must remain empty if nothing is provided."
    )
    armor_proficiencies_gain: list[ArmorProficiency] = Field(
        description="Must remain empty if nothing is provided."
    )
    attribute_increase: Optional[StatisticAndAny]

    def __init__(self, /, **data: Any):
        data["weapon_proficiencies_gain"] = list(
            filterfalse(
                ArmorProficiency.__contains__, data["armor_proficiencies_gain"]
            )
        )
        if (
            data["skill_proficiency_gain"] not in Skill
            and data["skill_proficiency_gain"] in ToolProficiency
        ):
            data["tool_proficiency_gain"] = data["skill_proficiency_gain"]
            data["skill_proficiency_gain"] = None
        try:
            super().__init__(**data)
        except Exception as e:
            raise e

    def assign_to(self, blueprint: Blueprint) -> Blueprint:
        """Assign this feature to a blueprint.

        The base implementation adds the feature to other_active_abilities.
        Subclasses can override this to modify other blueprint fields.

        Args:
            blueprint: The character blueprint to modify

        Returns:
            A new blueprint with this feature applied
        """
        return type(blueprint)(
            other_active_abilities=blueprint.other_active_abilities
            + (f"{self.name}: {self.description}",)
        )
