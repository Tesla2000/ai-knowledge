from __future__ import annotations

from collections.abc import Mapping
from typing import Annotated
from typing import Any
from typing import Optional

from dnd_character_creator.character.armor.names import ArmorName
from dnd_character_creator.character.feature.feats import FeatName
from dnd_character_creator.character.magical_item.item import MagicalItem
from dnd_character_creator.character.race.race import Race
from dnd_character_creator.character.race.subraces import Subrace
from dnd_character_creator.character.spells.spells import Spells
from dnd_character_creator.character.stats import Stats
from dnd_character_creator.choices.alignment import Alignment
from dnd_character_creator.choices.background_creatrion.background import (
    Background,
)
from dnd_character_creator.choices.class_creation.character_class import (
    AnySubclass,
)
from dnd_character_creator.choices.class_creation.character_class import Class
from dnd_character_creator.choices.equipment_creation.weapons import WeaponName
from dnd_character_creator.choices.language import Language
from dnd_character_creator.choices.sex import Sex
from dnd_character_creator.choices.stats_creation.statistic import Statistic
from dnd_character_creator.other_profficiencies import ArmorProficiency
from dnd_character_creator.other_profficiencies import GamingSet
from dnd_character_creator.other_profficiencies import MusicalInstrument
from dnd_character_creator.other_profficiencies import ToolProficiency
from dnd_character_creator.other_profficiencies import WeaponProficiency
from dnd_character_creator.skill_proficiency import Skill
from frozendict import frozendict
from pydantic import AfterValidator
from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from pydantic import NonNegativeInt
from pydantic import PositiveInt


def _conv_to_frozendict(value: Any) -> Any:
    if not isinstance(value, Mapping):
        return value
    return frozendict(value)


def _language_not_any(language: Language) -> Language:
    if language == Language.ANY_OF_YOUR_CHOICE:
        raise ValueError(
            "Character language mustn't be any of your choice. Choose a languge"
        )
    return language


def _skill_not_any(skill: Skill) -> Skill:
    if skill == Skill.ANY_OF_YOUR_CHOICE:
        raise ValueError(
            "Character skill mustn't be any of your choice. Choose a skill"
        )
    return skill


def _feat_not_any(feat: FeatName) -> FeatName:
    if feat in FeatName.not_choosables():
        raise ValueError(
            "Character feat mustn't be any of your choice. Choose a feat"
        )
    return feat


def _tool_proficiency_not_any(
    tool: ToolProficiency | GamingSet | MusicalInstrument,
) -> ToolProficiency | GamingSet | MusicalInstrument:
    if (
        isinstance(tool, ToolProficiency)
        and tool == ToolProficiency.ANY_OF_YOUR_CHOICE
    ):
        raise ValueError(
            "Character tool proficiency mustn't be any of your choice. Choose a tool"
        )
    if isinstance(tool, GamingSet) and tool == GamingSet.ANY_OF_YOUR_CHOICE:
        raise ValueError(
            "Character gaming set mustn't be any of your choice. Choose a gaming set"
        )
    if (
        isinstance(tool, MusicalInstrument)
        and tool == MusicalInstrument.ANY_OF_YOUR_CHOICE
    ):
        raise ValueError(
            "Character musical instrument mustn't be any of your choice. Choose a musical instrument"
        )
    return tool


def _weapon_proficiency_not_any(
    weapon: WeaponProficiency,
) -> WeaponProficiency:
    if weapon == WeaponProficiency.ANY_OF_YOUR_CHOICE:
        raise ValueError(
            "Character weapon proficiency mustn't be any of your choice. Choose a weapon"
        )
    return weapon


def _armor_proficiency_not_any(armor: ArmorProficiency) -> ArmorProficiency:
    if armor == ArmorProficiency.ANY_OF_YOUR_CHOICE:
        raise ValueError(
            "Character armor proficiency mustn't be any of your choice. Choose an armor type"
        )
    return armor


NotAnyLanguage = Annotated[Language, AfterValidator(_language_not_any)]
NotAnySkill = Annotated[Skill, AfterValidator(_skill_not_any)]
NotAnyFeat = Annotated[FeatName, AfterValidator(_feat_not_any)]
NotAnyToolProficiency = Annotated[
    ToolProficiency | GamingSet | MusicalInstrument,
    AfterValidator(_tool_proficiency_not_any),
]
NotAnyWeaponProficiency = Annotated[
    WeaponProficiency, AfterValidator(_weapon_proficiency_not_any)
]
NotAnyArmorProficiency = Annotated[
    ArmorProficiency, AfterValidator(_armor_proficiency_not_any)
]

ClassLevel = Annotated[int, Field(ge=1, le=20)]


class Character(BaseModel):
    model_config = ConfigDict(frozen=True)

    sex: Sex
    backstory: str
    level: ClassLevel
    age: PositiveInt
    classes: Annotated[
        Mapping[Class, PositiveInt], AfterValidator(_conv_to_frozendict)
    ] = frozendict()
    race: Race
    subrace: Subrace
    name: str
    background: Background
    alignment: Alignment
    stats: Stats
    health_base: PositiveInt = Field(exclude=True)
    height: PositiveInt
    weight: PositiveInt
    eye_color: str
    skin_color: str
    hairstyle: str
    appearance: str
    character_traits: str
    ideals: str
    bonds: str
    weaknesses: str
    dark_vision_range: NonNegativeInt
    base_description: Optional[str] = None
    feats: frozenset[NotAnyFeat] = Field(
        description="Feats from a list fitting description of the character if"
        " race is variant human at least one must be different "
        "than ability score improvement",
        default=frozenset(),
    )
    subclasses: tuple[AnySubclass, ...] = ()
    armors: tuple[ArmorName, ...] = Field(
        default=(),
        description="You would typically have clothes for spell casters. You "
        "have a total of 'amount_of_gold_for_equipment' to spend "
        "for both armor and weapons. Barbarians and Monks usually "
        "don't use armor either.",
    )
    weapons: tuple[WeaponName, ...] = Field(
        description="You would typically leave it empty for spell casters. "
        "You have a total of 'amount_of_gold_for_equipment' to "
        "spend for both armor and weapons.",
        default=(),
    )
    other_equipment: tuple[str, ...] = Field(
        default=(),
        description="All alchemical supplies, medicines, potions etc.",
    )
    spells: Spells = Field(default_factory=Spells)
    languages: frozenset[NotAnyLanguage] = frozenset()
    skill_proficiencies: frozenset[NotAnySkill] = Field(
        default=frozenset(),
        description="Skills the character is proficient in",
    )
    tool_proficiencies: frozenset[NotAnyToolProficiency] = Field(
        default=frozenset(), description="Tool proficiencies"
    )
    weapon_proficiencies: frozenset[NotAnyWeaponProficiency] = Field(
        default=frozenset(), description="Weapon proficiencies"
    )
    armor_proficiencies: frozenset[NotAnyArmorProficiency] = Field(
        default=frozenset(), description="Armor proficiencies"
    )
    speed: PositiveInt
    magical_items: tuple[MagicalItem, ...] = ()
    saving_throw_bonuses: Stats = Field(
        default=Stats(
            strength=0,
            dexterity=0,
            constitution=0,
            intelligence=0,
            wisdom=0,
            charisma=0,
        ),
        exclude=True,
    )
    stats_cup: Stats = Field(
        default=Stats(
            strength=20,
            dexterity=20,
            constitution=20,
            intelligence=20,
            wisdom=20,
            charisma=20,
        ),
        exclude=True,
    )
    ac_bonus: NonNegativeInt = Field(0, exclude=True)
    spell_save_dc_bonus: NonNegativeInt = Field(0, exclude=True)
    spellcasting_ability_bonus: NonNegativeInt = Field(0, exclude=True)
    saving_throw_proficiencies: tuple[Statistic, ...]
    other_active_abilities: tuple[str, ...]
