"""Component for formatting Blueprint data into structured text for AI prompts."""

from __future__ import annotations

from typing import Literal

from dnd.character.blueprint.blueprint import Blueprint
from dnd.character.spells.spells import Spells
from pydantic import BaseModel
from pydantic import Field


class BlueprintFormatter(BaseModel):
    """Formats Blueprint data into structured text suitable for AI prompts.

    This component provides a standardized way to present character information
    to AI models, with configurable sections and formatting options.

    Example:
        >>> formatter = BlueprintFormatter(
        ...     include_backstory=True,
        ...     include_stats=True,
        ...     format_style="markdown"
        ... )
        >>> prompt_text = formatter.format(blueprint)
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

    def format(self, blueprint: Blueprint, system_prompt: str | None = None) -> str:
        """Format a Blueprint into structured text.

        Args:
            blueprint: The character blueprint to format.
            system_prompt: Optional system prompt to prepend. If not provided,
                uses the instance's system_prompt field.

        Returns:
            Formatted string representation of the blueprint.
        """
        sections = []

        # Add system prompt if provided
        prompt_to_use = (
            system_prompt if system_prompt is not None else self.system_prompt
        )
        if prompt_to_use:
            sections.append(prompt_to_use)

        # Identity
        identity_lines = self._format_identity(blueprint)
        if identity_lines:
            sections.append(self._section_header("Character Identity"))
            sections.extend(identity_lines)

        # Classes
        if self.include_classes and blueprint.classes:
            sections.append(self._section_header("Classes & Levels"))
            sections.extend(self._format_classes(blueprint))

        # Race
        if self.include_race and blueprint.race:
            sections.append(self._section_header("Race"))
            sections.extend(self._format_race(blueprint))

        # Background
        if self.include_background and blueprint.background:
            sections.append(self._section_header("Background"))
            sections.append(self._item(blueprint.background.value))

        # Alignment
        if self.include_alignment and blueprint.alignment:
            sections.append(self._section_header("Alignment"))
            sections.append(self._item(blueprint.alignment.value))

        # Backstory
        if self.include_backstory and blueprint.backstory:
            sections.append(self._section_header("Backstory"))
            sections.append(self._item(blueprint.backstory))

        # Stats
        if self.include_stats and blueprint.stats:
            sections.append(self._section_header("Ability Scores"))
            sections.extend(self._format_stats(blueprint))

        # Skills
        if self.include_skills and blueprint.skill_proficiencies:
            sections.append(self._section_header("Skill Proficiencies"))
            skills_str = ", ".join(
                skill.value for skill in blueprint.skill_proficiencies
            )
            sections.append(self._item(skills_str))

        # Equipment
        if self.include_equipment:
            equipment_lines = self._format_equipment(blueprint)
            if equipment_lines:
                sections.append(self._section_header("Current Equipment"))
                sections.extend(equipment_lines)

        # Spells
        if self.include_spells and blueprint.spells:
            sections.append(self._section_header("Spells"))
            sections.extend(self._format_spells(blueprint.spells))

        # Feats
        if self.include_feats and blueprint.feats:
            sections.append(self._section_header("Feats"))
            feats_str = ", ".join(feat.value for feat in blueprint.feats)
            sections.append(self._item(feats_str))

        return "\n".join(sections)

    def _section_header(self, title: str) -> str:
        """Format a section header based on format style."""
        if self.format_style == "markdown":
            return f"\n## {title}"
        else:
            return f"\n{title.upper()}"

    def _item(self, text: str, indent: int = 1) -> str:
        """Format an item with appropriate indentation."""
        prefix = "  " * indent
        return f"{prefix}{text}"

    def _format_identity(self, blueprint: Blueprint) -> list[str]:
        """Format identity information (name, sex, age)."""
        lines = []
        if self.include_name and blueprint.name:
            lines.append(self._item(f"Name: {blueprint.name}"))
        if self.include_sex and blueprint.sex:
            lines.append(self._item(f"Sex: {blueprint.sex.value}"))
        if self.include_age and blueprint.age:
            lines.append(self._item(f"Age: {blueprint.age}"))
        return lines

    def _format_classes(self, blueprint: Blueprint) -> list[str]:
        """Format class and level information."""
        lines = []
        for cls, level in blueprint.classes.items():
            lines.append(self._item(f"{cls.value}: Level {level}"))
        return lines

    def _format_race(self, blueprint: Blueprint) -> list[str]:
        """Format race and subrace information."""
        lines = [self._item(blueprint.race.value)]  # type: ignore[union-attr]
        if blueprint.subrace:
            lines.append(self._item(f"Subrace: {blueprint.subrace.value}"))
        return lines

    def _format_stats(self, blueprint: Blueprint) -> list[str]:
        """Format ability scores."""
        return [
            self._item(f"Strength: {blueprint.stats.strength}"),  # type: ignore[union-attr]
            self._item(f"Dexterity: {blueprint.stats.dexterity}"),  # type: ignore[union-attr]
            self._item(f"Constitution: {blueprint.stats.constitution}"),  # type: ignore[union-attr]
            self._item(f"Intelligence: {blueprint.stats.intelligence}"),  # type: ignore[union-attr]
            self._item(f"Wisdom: {blueprint.stats.wisdom}"),  # type: ignore[union-attr]
            self._item(f"Charisma: {blueprint.stats.charisma}"),  # type: ignore[union-attr]
        ]

    def _format_equipment(self, blueprint: Blueprint) -> list[str]:
        """Format equipment information."""
        lines = []
        if blueprint.armors:
            armors_str = ", ".join(w.value for w in blueprint.armors)
            lines.append(self._item(f"Armors: {armors_str}"))
        if blueprint.weapons:
            weapons_str = ", ".join(w.value for w in blueprint.weapons)
            lines.append(self._item(f"Weapons: {weapons_str}"))
        if blueprint.other_equipment:
            others_str = ", ".join(str(item) for item in blueprint.other_equipment)
            lines.append(self._item(f"Other: {others_str}"))
        if blueprint.magical_items:
            items_str = ", ".join(item.name for item in blueprint.magical_items)
            lines.append(self._item(f"Magical Items: {items_str}"))
        return lines

    def _format_spells(self, spells: Spells) -> list[str]:
        """Format spell information."""
        lines = []
        if spells.cantrips:
            cantrips = ", ".join(c.value for c in spells.cantrips)
            lines.append(self._item(f"Cantrips: {cantrips}"))

        for level in range(1, 10):
            spells_at_level = spells.get_spell_level_by_index(level)  # type: ignore[arg-type]
            if spells_at_level:
                spells_str = ", ".join(s.value for s in spells_at_level)
                lines.append(self._item(f"Level {level}: {spells_str}"))

        return lines
