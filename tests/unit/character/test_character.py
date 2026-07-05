from __future__ import annotations

import pytest
from frozendict import frozendict
from pydantic import ValidationError

from dnd.character.character import Character
from dnd.character.character import _conv_to_frozendict
from dnd.character.class_levels import ClassLevels
from dnd.character.stats import Stats
from dnd.choices.alignment import Alignment
from dnd.choices.background_creatrion.background import Background
from dnd.choices.class_creation.character_class import Class
from dnd.choices.language import Language
from dnd.choices.sex import Sex
from dnd.character.feature.feats import FeatName
from dnd.other_profficiencies import (
    ArmorProficiency,
    GamingSet,
    MusicalInstrument,
    ToolProficiency,
    WeaponProficiency,
)
from dnd.skill_proficiency import Skill
from dnd.character.race.race import Race
from dnd.character.race.subraces import SubraceName

_STATS = Stats(
    strength=10,
    dexterity=10,
    constitution=10,
    intelligence=18,
    wisdom=10,
    charisma=10,
)

_BASE_KWARGS: dict[str, object] = dict(
    name="Alice",
    stats=_STATS,
    speed=30,
    dark_vision_range=0,
    saving_throw_proficiencies=(),
    other_active_abilities=(),
    sex=Sex.FEMALE,
    backstory="A brilliant mage.",
    level=1,
    age=25,
    race=Race.HUMAN,
    subrace=SubraceName.HUMAN_STANDARD_HUMAN_PLAYERSHANDBOOK,
    background=Background.SAGE,
    alignment=Alignment.CHAOTIC_GOOD,
    health_base=6,
    height=65,
    weight=130,
    eye_color="blue",
    skin_color="fair",
    hairstyle="long brown",
    appearance="tall and slender",
    character_traits="curious",
    ideals="knowledge",
    bonds="books",
    weaknesses="overconfident",
)


@pytest.mark.unit
class TestCharacterValidators:
    def test_language_not_any_raises(self) -> None:
        with pytest.raises(ValidationError, match="mustn't be any of your choice"):
            Character(
                **_BASE_KWARGS, languages=frozenset({Language.ANY_OF_YOUR_CHOICE})
            )

    def test_skill_not_any_raises(self) -> None:
        with pytest.raises(ValidationError, match="mustn't be any of your choice"):
            Character(
                **_BASE_KWARGS,
                skill_proficiencies=frozenset({Skill.ANY_OF_YOUR_CHOICE}),
            )

    def test_feat_not_any_raises(self) -> None:
        with pytest.raises(ValidationError, match="mustn't be any of your choice"):
            Character(**_BASE_KWARGS, feats=frozenset({FeatName.ANY_OF_YOUR_CHOICE}))

    def test_tool_proficiency_any_raises(self) -> None:
        with pytest.raises(ValidationError, match="mustn't be any of your choice"):
            Character(
                **_BASE_KWARGS,
                tool_proficiencies=frozenset({ToolProficiency.ANY_OF_YOUR_CHOICE}),
            )

    def test_gaming_set_any_raises(self) -> None:
        with pytest.raises(ValidationError, match="mustn't be any of your choice"):
            Character(
                **_BASE_KWARGS,
                tool_proficiencies=frozenset({GamingSet.ANY_OF_YOUR_CHOICE}),
            )

    def test_musical_instrument_any_raises(self) -> None:
        with pytest.raises(ValidationError, match="mustn't be any of your choice"):
            Character(
                **_BASE_KWARGS,
                tool_proficiencies=frozenset({MusicalInstrument.ANY_OF_YOUR_CHOICE}),
            )

    def test_weapon_proficiency_any_raises(self) -> None:
        with pytest.raises(ValidationError, match="mustn't be any of your choice"):
            Character(
                **_BASE_KWARGS,
                weapon_proficiencies=frozenset({WeaponProficiency.ANY_OF_YOUR_CHOICE}),
            )

    def test_armor_proficiency_any_raises(self) -> None:
        with pytest.raises(ValidationError, match="mustn't be any of your choice"):
            Character(
                **_BASE_KWARGS,
                armor_proficiencies=frozenset({ArmorProficiency.ANY_OF_YOUR_CHOICE}),
            )

    def test_classes_dict_input_converted_to_frozendict(self) -> None:
        char = Character(**_BASE_KWARGS, classes={Class.WIZARD: 1})
        assert isinstance(char.classes, frozendict)
        assert char.classes[Class.WIZARD] == 1

    def test_class_levels_input_converted(self) -> None:
        levels = ClassLevels()
        char = Character(**_BASE_KWARGS, classes=levels)
        assert isinstance(char.classes, dict)

    def test_valid_tool_proficiency_passes_validator(self) -> None:
        char = Character(
            **_BASE_KWARGS,
            tool_proficiencies=frozenset({ToolProficiency.HERBALISM_KIT}),
        )
        assert ToolProficiency.HERBALISM_KIT in char.tool_proficiencies

    def test_valid_armor_proficiency_passes_validator(self) -> None:
        char = Character(
            **_BASE_KWARGS,
            armor_proficiencies=frozenset({ArmorProficiency.LIGHT_ARMOR}),
        )
        assert ArmorProficiency.LIGHT_ARMOR in char.armor_proficiencies


@pytest.mark.unit
class TestConvToFrozendict:
    def test_non_mapping_returns_value_unchanged(self) -> None:
        assert _conv_to_frozendict(42) == 42

    def test_mapping_returns_frozendict(self) -> None:
        result = _conv_to_frozendict({"key": "value"})
        assert isinstance(result, frozendict)
