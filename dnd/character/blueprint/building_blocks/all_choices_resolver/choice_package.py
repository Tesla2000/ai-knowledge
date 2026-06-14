"""Package containing all choice selections for AI resolution."""

from __future__ import annotations

from dnd.character.feature.feats import FeatName
from dnd.choices.language import Language
from dnd.other_profficiencies import GamingSet
from dnd.other_profficiencies import MusicalInstrument
from dnd.other_profficiencies import ToolProficiency
from dnd.skill_proficiency import Skill
from pydantic import BaseModel
from pydantic import Field


class ChoicePackage(BaseModel):
    """Complete package of all choices to be made for a character.

    This schema is used by AI to make all character choices holistically
    in a single LLM call, allowing for more coherent and context-aware
    selections across all choice types.
    """

    # ANY_OF_YOUR_CHOICE placeholder replacements
    languages: list[Language] = Field(
        default_factory=list,
        description="Languages to replace ANY_OF_YOUR_CHOICE placeholders",
    )
    skill_proficiencies: list[Skill] = Field(
        default_factory=list,
        description="Skills to replace ANY_OF_YOUR_CHOICE placeholders",
    )
    feats: list[FeatName] = Field(
        default_factory=list,
        description="Feats to replace ANY_OF_YOUR_CHOICE placeholders "
        "(excluding ABILITY_SCORE_IMPROVEMENT)",
    )
    tool_proficiencies: list[ToolProficiency | GamingSet | MusicalInstrument] = Field(
        default_factory=list,
        description="Tool proficiencies to replace ANY_OF_YOUR_CHOICE placeholders",
    )

    # Skill selection from available pool
    selected_skills: list[Skill] = Field(
        default_factory=list,
        description="Skills selected from skills_to_choose_from pool",
    )

    # Equipment choices
    # Note: Equipment choices are complex and may need separate handling
    # For now, we'll let EquipmentChooser handle this separately
