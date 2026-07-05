from __future__ import annotations

import pytest

from dnd.character.armor.armor import Armor
from dnd.character.armor.category import ArmorCategory
from dnd.character.armor.names import ArmorName
from dnd.character.character import Character
from dnd.character.race.race import Race
from dnd.character.race.subraces import SubraceName
from dnd.character.stats import Stats
from dnd.choices.alignment import Alignment
from dnd.choices.background_creatrion.background import Background
from dnd.choices.class_creation.character_class import Class
from dnd.choices.sex import Sex
from dnd.other_profficiencies import ArmorProficiency

_STATS_HIGH_DEX = Stats(
    strength=10,
    dexterity=16,
    constitution=10,
    intelligence=10,
    wisdom=10,
    charisma=10,
)
_STATS_MONK = Stats(
    strength=10,
    dexterity=12,
    constitution=10,
    intelligence=10,
    wisdom=14,
    charisma=10,
)
_STATS_BARBARIAN = Stats(
    strength=10,
    dexterity=12,
    constitution=14,
    intelligence=10,
    wisdom=10,
    charisma=10,
)

_BASE_KWARGS: dict[str, object] = dict(
    name="Test",
    speed=30,
    dark_vision_range=0,
    saving_throw_proficiencies=(),
    other_active_abilities=(),
    sex=Sex.MALE,
    backstory="A warrior.",
    level=1,
    age=20,
    race=Race.HUMAN,
    subrace=SubraceName.HUMAN_STANDARD_HUMAN_PLAYERSHANDBOOK,
    background=Background.SOLDIER,
    alignment=Alignment.TRUE_NEUTRAL,
    health_base=10,
    height=70,
    weight=180,
    eye_color="brown",
    skin_color="tan",
    hairstyle="short",
    appearance="muscular",
    character_traits="brave",
    ideals="justice",
    bonds="family",
    weaknesses="impulsive",
)


@pytest.mark.unit
class TestArmorCalcAC:
    def test_heavy_armor_no_dex_bonus(self) -> None:
        char = Character(
            **_BASE_KWARGS,
            stats=_STATS_HIGH_DEX,
            armor_proficiencies=frozenset({ArmorProficiency.HEAVY_ARMOR}),
        )
        armor = Armor(
            name=ArmorName.CHAIN_MAIL,
            category=ArmorCategory.HEAVY,
            disadvantage_on_stealth=True,
            base_ac=16,
            cost=75.0,
        )
        assert armor.calc_ac(char) == 16

    def test_medium_armor_capped_dex_bonus(self) -> None:
        char = Character(
            **_BASE_KWARGS,
            stats=_STATS_HIGH_DEX,
            armor_proficiencies=frozenset({ArmorProficiency.MEDIUM_ARMOR}),
        )
        armor = Armor(
            name=ArmorName.HALFPLATE,
            category=ArmorCategory.MEDIUM,
            disadvantage_on_stealth=True,
            base_ac=15,
            cost=750.0,
        )
        assert armor.calc_ac(char) == 17

    def test_monk_adds_wisdom_bonus(self) -> None:
        char = Character(
            **_BASE_KWARGS,
            stats=_STATS_MONK,
            classes={Class.MONK: 1},
        )
        armor = Armor(
            name=ArmorName.CLOTHES,
            category=ArmorCategory.NONE,
            disadvantage_on_stealth=False,
            base_ac=10,
            cost=1.0,
        )
        assert armor.calc_ac(char) == 13

    def test_barbarian_adds_constitution_bonus(self) -> None:
        char = Character(
            **_BASE_KWARGS,
            stats=_STATS_BARBARIAN,
            classes={Class.BARBARIAN: 1},
        )
        armor = Armor(
            name=ArmorName.CLOTHES,
            category=ArmorCategory.NONE,
            disadvantage_on_stealth=False,
            base_ac=10,
            cost=1.0,
        )
        assert armor.calc_ac(char) == 13
