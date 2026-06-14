from __future__ import annotations

from dnd.choices.language import Language
from dnd.other_profficiencies import GamingSet
from dnd.other_profficiencies import MusicalInstrument
from dnd.other_profficiencies import ToolProficiency
from dnd.skill_proficiency import SkillAndAny
from pydantic import BaseModel
from pydantic import Field


class BackgroundTemplate(BaseModel):
    skills: list[SkillAndAny] = Field(
        description="Skill proficiencies gained with background. Empty list if None."
    )
    tools: list[ToolProficiency | GamingSet | MusicalInstrument] = Field(
        description="Tool proficiencies gained with background. "
        "Empty list if None. "
        "Mind options you are provided 'Vehicles (Land)' should be"
        " 'Land vehicles' for example."
    )
    languages: list[Language] = Field(
        description="Languages gained with background. "
        "If 2 or more of your choice place as many values in a "
        "list. For example for 'Two of your choice' it is "
        "['Any of your choice', 'Any of your choice']. "
        "Empty list if None."
    )

    def __init__(self, /, **data: object):
        data["tools"] = list(map(str.capitalize, data["tools"]))
        super().__init__(**data)
