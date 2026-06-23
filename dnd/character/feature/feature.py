from __future__ import annotations

from dnd.character.ability import Ability
from dnd.choices.stats_creation.statistic import StatisticAndAny
from dnd.other_profficiencies import ArmorProficiency
from dnd.other_profficiencies import GamingSet
from dnd.other_profficiencies import MusicalInstrument
from dnd.other_profficiencies import ToolProficiency
from dnd.other_profficiencies import WeaponProficiency
from dnd.skill_proficiency import Skill
from pydantic import BaseModel
from pydantic import Field


class Feature(BaseModel):
    source: str | None
    ability: Ability | None
    skill_proficiency_gain: Skill | None
    skill_expertise_gain: Skill | None = Field(
        description="The same as double proficiency."
    )
    tool_proficiency_gain: ToolProficiency | None
    instrument_proficiency_gain: MusicalInstrument | None
    gaming_set_proficiency_gain: GamingSet | None
    weapon_proficiencies_gain: list[WeaponProficiency] = Field(
        description="Must remain empty if nothing is provided."
    )
    armor_proficiencies_gain: list[ArmorProficiency] = Field(
        description="Must remain empty if nothing is provided."
    )
    attribute_increase: StatisticAndAny | None

    def __init__(self, /, **data: object):
        armor_raw = data.get("armor_proficiencies_gain")
        armor_list = list(armor_raw) if isinstance(armor_raw, list) else []
        data["weapon_proficiencies_gain"] = [
            x for x in armor_list if x not in ArmorProficiency
        ]
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
