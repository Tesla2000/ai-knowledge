from __future__ import annotations

import pytest
from pydantic import Field, create_model

from dnd.character.armor.names import ArmorName
from dnd.character.blueprint.blueprint_formatter import BlueprintFormatter
from dnd.character.blueprint.state import Blueprint
from dnd.character.class_levels import ClassLevels
from dnd.character.feature.feats import FeatName
from dnd.character.magical_item.item import MagicalItem
from dnd.character.magical_item.level import Level
from dnd.character.magical_item.source import Source
from dnd.character.race.race import Race
from dnd.character.race.subraces import SubraceName
from dnd.character.spells.spell_slots import Cantrip, FirstLevel
from dnd.character.spells.spells import Spells
from dnd.character.stats import Stats
from dnd.choices.alignment import Alignment
from dnd.choices.background_creatrion.background import Background
from dnd.choices.equipment_creation.weapons import WeaponName
from dnd.choices.sex import Sex
from dnd.skill_proficiency import Skill


_WizardLevels2 = create_model("_WizardLevels2", __base__=ClassLevels, wizard=(int, 2))

_DEFAULT_STATS = Stats(
    strength=10,
    dexterity=10,
    constitution=10,
    intelligence=16,
    wisdom=10,
    charisma=10,
)


class _FormatterState(Blueprint):
    """Blueprint subclass with all fields needed by BlueprintFormatter."""

    classes: ClassLevels = Field(default_factory=_WizardLevels2)
    name: str = "Elara"
    sex: Sex = Sex.FEMALE
    age: int = 25
    race: Race = Race.HUMAN
    subrace: SubraceName = SubraceName.HUMAN_STANDARD_HUMAN_PLAYERSHANDBOOK
    speed: int = 30
    dark_vision_range: int = 0
    stats: Stats = Field(default=_DEFAULT_STATS)
    background: Background = Background.SAGE
    alignment: Alignment = Alignment.CHAOTIC_GOOD
    backstory: str = "A brilliant wizard seeking ancient knowledge."


@pytest.fixture(scope="module")
def built_character() -> _FormatterState:
    return _FormatterState()


@pytest.mark.unit
class TestBlueprintFormatter:
    def test_format_returns_string(self, built_character: _FormatterState) -> None:
        formatter = BlueprintFormatter()
        output = formatter.format(built_character)
        assert isinstance(output, str)
        assert len(output) > 0

    def test_format_includes_name(self, built_character: _FormatterState) -> None:
        formatter = BlueprintFormatter()
        output = formatter.format(built_character)
        assert built_character.name in output

    def test_format_includes_classes(self, built_character: _FormatterState) -> None:
        formatter = BlueprintFormatter()
        output = formatter.format(built_character)
        assert "Classes" in output
        assert "Wizard" in output

    def test_format_includes_race(self, built_character: _FormatterState) -> None:
        formatter = BlueprintFormatter()
        output = formatter.format(built_character)
        assert "Race" in output

    def test_format_includes_background(self, built_character: _FormatterState) -> None:
        formatter = BlueprintFormatter()
        output = formatter.format(built_character)
        assert "Background" in output

    def test_format_includes_alignment(self, built_character: _FormatterState) -> None:
        formatter = BlueprintFormatter()
        output = formatter.format(built_character)
        assert "Alignment" in output

    def test_format_includes_backstory(self, built_character: _FormatterState) -> None:
        formatter = BlueprintFormatter()
        output = formatter.format(built_character)
        assert "Backstory" in output

    def test_format_includes_stats(self, built_character: _FormatterState) -> None:
        formatter = BlueprintFormatter()
        output = formatter.format(built_character)
        assert "Ability Scores" in output
        assert "Strength" in output

    def test_format_includes_spells_with_cantrips(
        self, built_character: _FormatterState
    ) -> None:
        char_with_cantrip = built_character.model_copy(
            update={"spells": Spells(cantrips=(Cantrip.FIRE_BOLT,))}
        )
        formatter = BlueprintFormatter()
        output = formatter.format(char_with_cantrip)
        assert "Cantrips" in output

    def test_format_includes_spells_with_level_spells(
        self, built_character: _FormatterState
    ) -> None:
        char_with_spells = built_character.model_copy(
            update={"spells": Spells(first_level_spells=(FirstLevel.MAGIC_MISSILE,))}
        )
        formatter = BlueprintFormatter()
        output = formatter.format(char_with_spells)
        assert "Level 1" in output

    def test_format_with_system_prompt(self, built_character: _FormatterState) -> None:
        formatter = BlueprintFormatter(system_prompt="CUSTOM PROMPT")
        output = formatter.format(built_character)
        assert "CUSTOM PROMPT" in output

    def test_format_system_prompt_parameter_overrides_field(
        self, built_character: _FormatterState
    ) -> None:
        formatter = BlueprintFormatter(system_prompt="FIELD PROMPT")
        output = formatter.format(built_character, system_prompt="PARAM PROMPT")
        assert "PARAM PROMPT" in output
        assert "FIELD PROMPT" not in output

    def test_format_plain_style_no_markdown(
        self, built_character: _FormatterState
    ) -> None:
        formatter = BlueprintFormatter(format_style="plain")
        output = formatter.format(built_character)
        assert "## " not in output

    def test_format_with_feats(self, built_character: _FormatterState) -> None:
        char_with_feat = built_character.model_copy(update={"feats": (FeatName.ALERT,)})
        formatter = BlueprintFormatter()
        output = formatter.format(char_with_feat)
        assert "Feats" in output

    def test_format_with_weapons(self, built_character: _FormatterState) -> None:
        char_with_weapon = built_character.model_copy(
            update={"weapons": (WeaponName.DAGGER,)}
        )
        formatter = BlueprintFormatter()
        output = formatter.format(char_with_weapon)
        assert "Weapons" in output

    def test_format_with_armors(self, built_character: _FormatterState) -> None:
        char_with_armor = built_character.model_copy(
            update={"armors": (ArmorName.CLOTHES,)}
        )
        formatter = BlueprintFormatter()
        output = formatter.format(char_with_armor)
        assert "Armors" in output

    def test_format_with_other_equipment(
        self, built_character: _FormatterState
    ) -> None:
        char_with_equipment = built_character.model_copy(
            update={"other_equipment": ("Rope",)}
        )
        formatter = BlueprintFormatter()
        output = formatter.format(char_with_equipment)
        assert "Other" in output

    def test_format_with_magical_items(self, built_character: _FormatterState) -> None:
        item = MagicalItem(
            name="Ring of Protection",
            description="A magic ring.",
            level=Level.UNCOMMON,
            source=Source.DMG,
            attuned=True,
        )
        char_with_items = built_character.model_copy(update={"magical_items": (item,)})
        formatter = BlueprintFormatter()
        output = formatter.format(char_with_items)
        assert "Magical Items" in output
        assert "Ring of Protection" in output

    def test_format_with_skill_proficiencies(
        self, built_character: _FormatterState
    ) -> None:
        char_with_skills = built_character.model_copy(
            update={"skill_proficiencies": (Skill.ARCANA,)}
        )
        formatter = BlueprintFormatter()
        output = formatter.format(char_with_skills)
        assert "Skill Proficiencies" in output

    def test_format_exclude_all_fields(self, built_character: _FormatterState) -> None:
        formatter = BlueprintFormatter(
            include_name=False,
            include_sex=False,
            include_age=False,
            include_race=False,
            include_classes=False,
            include_background=False,
            include_alignment=False,
            include_backstory=False,
            include_stats=False,
            include_skills=False,
            include_equipment=False,
            include_spells=False,
            include_feats=False,
        )
        output = formatter.format(built_character)
        assert "## " not in output or output == ""
