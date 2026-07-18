import pytest

from dnd.character.class_levels import ClassLevels
from dnd.character.presentable_character import PresentableCharacter
from dnd.character.race.race import Race
from dnd.character.race.subraces import SubraceName
from dnd.character.stats import Stats
from dnd.choices.alignment import Alignment
from dnd.choices.background_creatrion.background import Background
from dnd.choices.sex import Sex
from dnd.character.health_modifier import DwarfHealthModifier
from dnd.character.health_modifier import ToughHealthModifier

_STATS = Stats(
    strength=10,
    dexterity=10,
    constitution=10,
    intelligence=18,
    wisdom=10,
    charisma=10,
)

_BASE_KWARGS: dict[str, object] = dict(
    name="TestChar",
    stats=_STATS,
    speed=30,
    dark_vision_range=0,
    saving_throw_proficiencies=(),
    other_active_abilities=(),
    sex=Sex.FEMALE,
    backstory="A test character.",
    age=25,
    race=Race.HUMAN,
    subrace=SubraceName.HUMAN_STANDARD_HUMAN_PLAYERSHANDBOOK,
    background=Background.SAGE,
    alignment=Alignment.CHAOTIC_GOOD,
    health_base=12,
    height=65,
    weight=130,
    eye_color="blue",
    skin_color="fair",
    hairstyle="long",
    appearance="slender",
    character_traits="curious",
    ideals="knowledge",
    bonds="books",
    weaknesses="overconfident",
)


@pytest.mark.unit
class TestPresentableCharacterNonCaster:
    def test_no_classes_spellcasting_ability_is_none(self) -> None:
        char = PresentableCharacter(**_BASE_KWARGS)
        assert char.spellcasting_ability is None

    def test_no_classes_spell_attack_bonus_is_none(self) -> None:
        char = PresentableCharacter(**_BASE_KWARGS)
        assert char.spell_attack_bonus is None

    def test_no_classes_n_prepared_spells_returns_level(self) -> None:
        char = PresentableCharacter(**_BASE_KWARGS)
        assert char.n_prepared_spells == char.level


_LEVELED_KWARGS: dict[str, object] = {**_BASE_KWARGS, "classes": ClassLevels(fighter=2)}


@pytest.mark.unit
class TestPresentableCharacterHealth:
    def test_health_with_tough_modifier(self) -> None:
        base_char = PresentableCharacter(**_LEVELED_KWARGS)
        tough_char = PresentableCharacter(
            **_LEVELED_KWARGS,
            health_modifiers=(ToughHealthModifier(),),
        )
        assert tough_char.health == base_char.health + base_char.level * 2

    def test_health_with_dwarf_modifier(self) -> None:
        base_char = PresentableCharacter(**_LEVELED_KWARGS)
        dwarf_char = PresentableCharacter(
            **_LEVELED_KWARGS,
            health_modifiers=(DwarfHealthModifier(),),
        )
        assert dwarf_char.health == base_char.health + base_char.level
