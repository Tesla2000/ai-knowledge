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
    source: str | None = None
    ability: Ability | None = None
    skill_proficiency_gain: Skill | None = None
    skill_expertise_gain: Skill | None = Field(
        default=None, description="The same as double proficiency."
    )
    tool_proficiency_gain: ToolProficiency | None = None
    instrument_proficiency_gain: MusicalInstrument | None = None
    gaming_set_proficiency_gain: GamingSet | None = None
    weapon_proficiencies_gain: list[WeaponProficiency] = Field(
        default_factory=list, description="Must remain empty if nothing is provided."
    )
    armor_proficiencies_gain: list[ArmorProficiency] = Field(
        default_factory=list, description="Must remain empty if nothing is provided."
    )
    attribute_increase: StatisticAndAny | None = None
