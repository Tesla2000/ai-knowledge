"""Component for formatting blueprint data into structured text for AI prompts."""

from typing import Literal

from dnd.character.blueprint.states.state import _BPT
from dnd.character.spells.spells import Spells
from pydantic import BaseModel
from pydantic import Field


class BlueprintFormatter(BaseModel):
    """Formats blueprint data into structured text suitable for AI prompts."""

    include_name: bool = Field(default=True)
    include_sex: bool = Field(default=True)
    include_age: bool = Field(default=True)
    include_race: bool = Field(default=True)
    include_classes: bool = Field(default=True)
    include_background: bool = Field(default=True)
    include_alignment: bool = Field(default=True)
    include_backstory: bool = Field(default=True)
    include_stats: bool = Field(default=True)
    include_skills: bool = Field(default=True)
    include_equipment: bool = Field(default=True)
    include_spells: bool = Field(default=True)
    include_feats: bool = Field(default=True)

    format_style: Literal["plain", "markdown"] = Field(default="markdown")
    system_prompt: str = Field(default="")

    def format(
        self,
        state: _BPT,
        system_prompt: str | None = None,
    ) -> str:
        """Format a blueprint state into structured text."""
        sections: list[str] = []

        prompt_to_use = (
            system_prompt if system_prompt is not None else self.system_prompt
        )
        if prompt_to_use:
            sections.append(prompt_to_use)

        identity_lines = self._format_identity(state)
        if identity_lines:
            sections.append(self._section_header("Character Identity"))
            sections.extend(identity_lines)

        if self.include_classes and state.classes.total_level() > 0:
            sections.append(self._section_header("Classes & Levels"))
            for cls, level in state.classes.all_levels():
                sections.append(self._item(f"{cls.value}: Level {level}"))

        if self.include_race and state.race is not None:
            sections.append(self._section_header("Race"))
            sections.append(self._item(state.race.value))
            if state.subrace is not None:
                sections.append(self._item(f"Subrace: {state.subrace.value}"))

        cd = state.character_data
        if self.include_background and cd is not None and cd.background is not None:
            sections.append(self._section_header("Background"))
            sections.append(self._item(cd.background.value))

        if self.include_alignment and cd is not None and cd.alignment is not None:
            sections.append(self._section_header("Alignment"))
            sections.append(self._item(cd.alignment.value))

        if self.include_backstory and cd is not None and cd.backstory is not None:
            sections.append(self._section_header("Backstory"))
            sections.append(self._item(cd.backstory))

        if self.include_stats and state.stats is not None:
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

        if self.include_skills and state.skill_proficiencies:
            sections.append(self._section_header("Skill Proficiencies"))
            skills_str = ", ".join(skill.value for skill in state.skill_proficiencies)
            sections.append(self._item(skills_str))

        if self.include_equipment:
            equipment_lines = self._format_equipment(state)
            if equipment_lines:
                sections.append(self._section_header("Current Equipment"))
                sections.extend(equipment_lines)

        if self.include_spells:
            spell_lines = self._format_spells(state.spells)
            if spell_lines:
                sections.append(self._section_header("Spells"))
                sections.extend(spell_lines)

        if self.include_feats and state.feats:
            sections.append(self._section_header("Feats"))
            feats_str = ", ".join(feat.value for feat in state.feats)
            sections.append(self._item(feats_str))

        return "\n".join(sections)

    def _section_header(self, title: str) -> str:
        if self.format_style == "markdown":
            return f"\n## {title}"
        return f"\n{title.upper()}"

    def _item(self, text: str, indent: int = 1) -> str:
        return f"{'  ' * indent}{text}"

    def _format_identity(self, state: _BPT) -> list[str]:
        lines: list[str] = []
        cd = state.character_data
        if self.include_name and cd is not None and cd.name is not None:
            lines.append(self._item(f"Name: {cd.name}"))
        if self.include_sex and cd is not None and cd.sex is not None:
            lines.append(self._item(f"Sex: {cd.sex.value}"))
        if self.include_age and cd is not None and cd.age is not None:
            lines.append(self._item(f"Age: {cd.age}"))
        return lines

    def _format_equipment(self, state: _BPT) -> list[str]:
        lines: list[str] = []
        if state.armors:
            lines.append(
                self._item(f"Armors: {', '.join(w.value for w in state.armors)}")
            )
        if state.weapons:
            lines.append(
                self._item(f"Weapons: {', '.join(w.value for w in state.weapons)}")
            )
        if state.other_equipment:
            lines.append(self._item(f"Other: {', '.join(state.other_equipment)}"))
        if state.magical_items:
            lines.append(
                self._item(
                    f"Magical Items: {', '.join(item.name for item in state.magical_items)}"
                )
            )
        return lines

    def _format_spells(self, spells: Spells) -> list[str]:
        lines: list[str] = []
        for level, spells_at_level in enumerate(spells.get_spells_by_level()):
            if level == 0:
                if spells_at_level:
                    lines.append(
                        self._item(
                            f"Cantrips: {', '.join(c.value for c in spells_at_level)}"
                        )
                    )
            elif spells_at_level:
                lines.append(
                    self._item(
                        f"Level {level}: {', '.join(s.value for s in spells_at_level)}"
                    )
                )
        return lines
