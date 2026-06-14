from __future__ import annotations

from itertools import filterfalse

from dnd.other_profficiencies import ArmorProficiency
from dnd.other_profficiencies import GamingSet
from dnd.other_profficiencies import MusicalInstrument
from dnd.other_profficiencies import ToolProficiency
from dnd.other_profficiencies import WeaponProficiency
from dnd.skill_proficiency import Skill
from pydantic import BaseModel
from pydantic import Field


class MainClassTemplate(BaseModel):
    obligatory_skills: list[Skill] = Field(
        description="A list of skills provided by class.", default_factory=list
    )
    skills_to_choose_from: list[Skill] = Field(
        description="A list of skills from which skills can be chosen.",
        default_factory=list,
    )
    n_skills: int = Field(
        description="Number of skills that can be chosen from skills to choose from.",
        default=0,
    )
    tools: list[ToolProficiency | GamingSet | MusicalInstrument] = Field(
        description="Tool proficiencies gained with class. Empty list if None."
    )
    armor: list[ArmorProficiency] = Field(
        description="Armor proficiencies gained with class. Empty list if None."
    )
    weapons: list[WeaponProficiency] = Field(
        description="Weapons proficiencies gained with class. Empty list if None."
    )

    def __init__(self, /, **data: object):
        data["tools"] = list(map(str.capitalize, data["tools"]))
        data["armor"] = list(
            " ".join(map(str.capitalize, prof.split())) for prof in data["armor"]
        )
        data["armor"] = list(filterfalse("None".__eq__, data["armor"]))
        data["weapons"] = list(prof.rstrip("s") for prof in data["weapons"])
        data["weapons"] = list(
            " ".join(map(str.capitalize, prof.split())) for prof in data["weapons"]
        )
        super().__init__(**data)
