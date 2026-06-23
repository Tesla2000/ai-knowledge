"""Component for formatting blueprint data into structured text for AI prompts."""

from __future__ import annotations
from typing import Literal

from dnd.character.blueprint.state import BlueprintProtocol
from dnd.character.blueprint.state import HasAge
from dnd.character.blueprint.state import HasAlignment
from dnd.character.blueprint.state import HasBackground
from dnd.character.blueprint.state import HasBackstory
from dnd.character.blueprint.state import HasClasses
from dnd.character.blueprint.state import HasArmors
from dnd.character.blueprint.state import HasFeats
from dnd.character.blueprint.state import HasMagicalItems
from dnd.character.blueprint.state import HasName
from dnd.character.blueprint.state import HasOtherEquipment
from dnd.character.blueprint.state import HasRace
from dnd.character.blueprint.state import HasSex
from dnd.character.blueprint.state import HasSkillProficiencies
from dnd.character.blueprint.state import HasSpells
from dnd.character.blueprint.state import HasStats
from dnd.character.blueprint.state import HasWeapons
from dnd.character.spells.spells import Spells
from pydantic import BaseModel
from pydantic import Field


class BlueprintFormatter(BaseModel):
    """Formats blueprint data into structured text suitable for AI prompts.

    Example:
        >>> formatter = BlueprintFormatter(
        ...     include_backstory=True,
        ...     include_stats=True,
        ...     format_style="markdown"
        ... )
        >>> prompt_text = formatter.format(state)
    """

    include_name: bool = Field(default=True, description="Include character name")
    include_sex: bool = Field(default=True, description="Include character sex")
    include_age: bool = Field(default=True, description="Include character age")
    include_race: bool = Field(default=True, description="Include race and subrace")
    include_classes: bool = Field(
        default=True, description="Include class and level information"
    )
    include_background: bool = Field(
        default=True, description="Include character background"
    )
    include_alignment: bool = Field(
        default=True, description="Include character alignment"
    )
    include_backstory: bool = Field(
        default=True, description="Include character backstory"
    )
    include_stats: bool = Field(default=True, description="Include ability scores")
    include_skills: bool = Field(
        default=True, description="Include skill proficiencies"
    )
    include_equipment: bool = Field(
        default=True, description="Include current equipment"
    )
    include_spells: bool = Field(default=True, description="Include spell information")
    include_feats: bool = Field(default=True, description="Include feats")

    format_style: Literal["plain", "markdown"] = Field(
        default="markdown",
        description="Output format style (plain text or markdown)",
    )

    system_prompt: str = Field(
        default="",
        description="Optional custom system prompt to prepend to the formatted output",
    )

    def format(self, state: BlueprintProtocol, system_prompt: str | None = None) -> str:
        """Format a blueprint state into structured text."""
        sections = []

        prompt_to_use = (
            system_prompt if system_prompt is not None else self.system_prompt
        )
        if prompt_to_use:
            sections.append(prompt_to_use)

        identity_lines = self._format_identity(state)
        if identity_lines:
            sections.append(self._section_header("Character Identity"))
            sections.extend(identity_lines)

        if self.include_classes and isinstance(state, HasClasses):
            sections.append(self._section_header("Classes & Levels"))
            for cls, level in state.classes.all_levels():
                sections.append(self._item(f"{cls.value}: Level {level}"))

        if self.include_race and isinstance(state, HasRace):
            sections.append(self._section_header("Race"))
            sections.append(self._item(state.race.value))
            sections.append(self._item(f"Subrace: {state.subrace.value}"))

        if self.include_background and isinstance(state, HasBackground):
            sections.append(self._section_header("Background"))
            sections.append(self._item(state.background.value))

        if self.include_alignment and isinstance(state, HasAlignment):
            sections.append(self._section_header("Alignment"))
            sections.append(self._item(state.alignment.value))

        if self.include_backstory and isinstance(state, HasBackstory):
            sections.append(self._section_header("Backstory"))
            sections.append(self._item(state.backstory))

        if self.include_stats and isinstance(state, HasStats):
            stats = state.stats
            sections.append(self._section_header("Ability Scores"))
            sections.extend(
                [
                    self._item(f"Strength: {stats.strength}"),
                    self._item(f"Dexterity: {stats.dexterity}"),
                    self._item(f"Constitution: {stats.constitution}"),
                    self._item(f"Intelligence: {stats.intelligence}"),
                    self._item(f"Wisdom: {stats.wisdom}"),
                    self._item(f"Charisma: {stats.charisma}"),
                ]
            )

        if self.include_skills and isinstance(state, HasSkillProficiencies):
            sections.append(self._section_header("Skill Proficiencies"))
            skills_str = ", ".join(skill.value for skill in state.skill_proficiencies)
            sections.append(self._item(skills_str))

        if self.include_equipment:
            equipment_lines = self._format_equipment(state)
            if equipment_lines:
                sections.append(self._section_header("Current Equipment"))
                sections.extend(equipment_lines)

        if self.include_spells and isinstance(state, HasSpells):
            sections.append(self._section_header("Spells"))
            sections.extend(self._format_spells(state.spells))

        if self.include_feats and isinstance(state, HasFeats) and state.feats:
            sections.append(self._section_header("Feats"))
            feats_str = ", ".join(feat.value for feat in state.feats)
            sections.append(self._item(feats_str))

        return "\n".join(sections)

    def _section_header(self, title: str) -> str:
        if self.format_style == "markdown":
            return f"\n## {title}"
        return f"\n{title.upper()}"

    def _item(self, text: str, indent: int = 1) -> str:
        prefix = "  " * indent
        return f"{prefix}{text}"

    def _format_identity(self, state: BlueprintProtocol) -> list[str]:
        lines = []
        if self.include_name and isinstance(state, HasName):
            lines.append(self._item(f"Name: {state.name}"))
        if self.include_sex and isinstance(state, HasSex):
            lines.append(self._item(f"Sex: {state.sex.value}"))
        if self.include_age and isinstance(state, HasAge):
            lines.append(self._item(f"Age: {state.age}"))
        return lines

    def _format_equipment(self, state: BlueprintProtocol) -> list[str]:
        lines = []
        if isinstance(state, HasArmors) and state.armors:
            armors_str = ", ".join(w.value for w in state.armors)
            lines.append(self._item(f"Armors: {armors_str}"))
        if isinstance(state, HasWeapons) and state.weapons:
            weapons_str = ", ".join(w.value for w in state.weapons)
            lines.append(self._item(f"Weapons: {weapons_str}"))
        if isinstance(state, HasOtherEquipment) and state.other_equipment:
            others_str = ", ".join(str(item) for item in state.other_equipment)
            lines.append(self._item(f"Other: {others_str}"))
        if isinstance(state, HasMagicalItems) and state.magical_items:
            items_str = ", ".join(item.name for item in state.magical_items)
            lines.append(self._item(f"Magical Items: {items_str}"))
        return lines

    def _format_spells(self, spells: Spells) -> list[str]:
        lines = []
        for level, spells_at_level in enumerate(spells.get_spells_by_level()):
            if level == 0:
                if spells_at_level:
                    cantrips = ", ".join(c.value for c in spells_at_level)
                    lines.append(self._item(f"Cantrips: {cantrips}"))
            elif spells_at_level:
                spells_str = ", ".join(s.value for s in spells_at_level)
                lines.append(self._item(f"Level {level}: {spells_str}"))
        return lines
