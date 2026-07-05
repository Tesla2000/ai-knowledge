from __future__ import annotations

from typing import ClassVar
from collections.abc import Iterator
from typing import Protocol
from typing import runtime_checkable

from dnd.character.armor.names import ArmorName
from dnd.character.magical_item.item import MagicalItem
from dnd.character.character import ClassLevel
from dnd.character.feature.feats import FeatName
from dnd.character.race.race import Race
from dnd.character.race.subraces import SubraceName
from dnd.character.spells.spells import Spells
from dnd.character.stats import Stats
from dnd.choices.alignment import Alignment
from dnd.choices.background_creatrion.background import Background
from dnd.choices.class_creation.character_class import AnySubclass
from dnd.choices.equipment_creation.weapons import WeaponName
from dnd.choices.language import Language
from dnd.choices.sex import Sex
from dnd.choices.stats_creation.statistic import Statistic
from dnd.other_profficiencies import ArmorProficiency
from dnd.other_profficiencies import GamingSet
from dnd.other_profficiencies import MusicalInstrument
from dnd.other_profficiencies import ToolProficiency
from dnd.other_profficiencies import WeaponProficiency
from dnd.skill_proficiency import Skill
from dnd.character.class_levels import ClassLevels
from pydantic import Field
from pydantic import NonNegativeInt, BaseModel, ConfigDict
from pydantic import PositiveInt

type Equipment = WeaponName | ArmorName | str


class Blueprint(BaseModel):
    """Accumulating character state during construction.

    Only carries fields with non-None defaults. Fields that start as None
    (race, stats, level, etc.) are added dynamically by deltas so that
    isinstance(state, HasXxx) guards work correctly — @runtime_checkable
    Protocol checks only verify attribute existence, not value.
    """

    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    classes: ClassLevels = Field(default_factory=ClassLevels)
    stats_cup: Stats = Field(
        default=Stats(
            strength=20,
            dexterity=20,
            constitution=20,
            intelligence=20,
            wisdom=20,
            charisma=20,
        )
    )
    saving_throw_bonuses: Stats = Field(
        default=Stats(
            strength=0,
            dexterity=0,
            constitution=0,
            intelligence=0,
            wisdom=0,
            charisma=0,
        )
    )
    initiative_bonus: int = 0
    ac_bonus: NonNegativeInt = 0
    spell_save_dc_bonus: NonNegativeInt = 0
    spellcasting_ability_bonus: NonNegativeInt = 0
    feats: tuple[FeatName, ...] = Field(default=())
    subclasses: tuple[AnySubclass, ...] = ()
    armors: tuple[ArmorName, ...] = ()
    weapons: tuple[WeaponName, ...] = ()
    other_equipment: tuple[str, ...] = ()
    spells: Spells = Field(default_factory=Spells)
    languages: tuple[Language, ...] = Field(default=())
    skill_proficiencies: tuple[Skill, ...] = Field(default=())
    tool_proficiencies: tuple[ToolProficiency | GamingSet | MusicalInstrument, ...] = (
        Field(default=())
    )
    weapon_proficiencies: frozenset[WeaponProficiency] = frozenset()
    armor_proficiencies: frozenset[ArmorProficiency] = frozenset()
    magical_items: tuple[MagicalItem, ...] = ()
    saving_throw_proficiencies: tuple[Statistic, ...] = ()
    other_active_abilities: tuple[str, ...] = ()
    n_stat_choices: NonNegativeInt = 0
    n_skill_choices: NonNegativeInt = 0
    skills_to_choose_from: frozenset[Skill] = Field(default_factory=frozenset)
    equipment_choices: tuple[tuple[Equipment, ...], ...] = ()


@runtime_checkable
class BlueprintProtocol(Protocol):
    def __iter__(self) -> Iterator[tuple[str, object]]: ...


@runtime_checkable
class HasLevel(BlueprintProtocol, Protocol):
    level: ClassLevel


@runtime_checkable
class HasStats(BlueprintProtocol, Protocol):
    stats: Stats


@runtime_checkable
class HasName(BlueprintProtocol, Protocol):
    name: str


@runtime_checkable
class HasAge(BlueprintProtocol, Protocol):
    age: PositiveInt


@runtime_checkable
class HasSex(BlueprintProtocol, Protocol):
    sex: Sex


@runtime_checkable
class HasNStatChoices(BlueprintProtocol, Protocol):
    n_stat_choices: int


@runtime_checkable
class HasNSkillChoices(BlueprintProtocol, Protocol):
    n_skill_choices: int


@runtime_checkable
class HasWeapons(BlueprintProtocol, Protocol):
    weapons: tuple[WeaponName, ...]


@runtime_checkable
class HasArmors(BlueprintProtocol, Protocol):
    armors: tuple[ArmorName, ...]


@runtime_checkable
class HasOtherEquipment(BlueprintProtocol, Protocol):
    other_equipment: tuple[str, ...]


@runtime_checkable
class HasEquipmentChoices(BlueprintProtocol, Protocol):
    equipment_choices: tuple[tuple[Equipment, ...], ...]


@runtime_checkable
class HasFeats(BlueprintProtocol, Protocol):
    feats: tuple[FeatName, ...]


@runtime_checkable
class HasAlignment(BlueprintProtocol, Protocol):
    alignment: Alignment


@runtime_checkable
class HasBackground(BlueprintProtocol, Protocol):
    background: Background


@runtime_checkable
class HasRace(BlueprintProtocol, Protocol):
    race: Race
    subrace: SubraceName
    speed: PositiveInt
    dark_vision_range: NonNegativeInt


@runtime_checkable
class HasLanguages(BlueprintProtocol, Protocol):
    languages: tuple[Language, ...]


@runtime_checkable
class HasSkillProficiencies(BlueprintProtocol, Protocol):
    skill_proficiencies: tuple[Skill, ...]


@runtime_checkable
class HasSkillsToChooseFrom(BlueprintProtocol, Protocol):
    skills_to_choose_from: frozenset[Skill]


@runtime_checkable
class HasToolProficiencies(BlueprintProtocol, Protocol):
    tool_proficiencies: tuple[ToolProficiency | GamingSet | MusicalInstrument, ...]


@runtime_checkable
class HasClasses(BlueprintProtocol, Protocol):
    classes: ClassLevels


@runtime_checkable
class HasHealthBase(BlueprintProtocol, Protocol):
    health_base: int


@runtime_checkable
class HasSubclasses(BlueprintProtocol, Protocol):
    subclasses: tuple[AnySubclass, ...]


@runtime_checkable
class HasSpells(BlueprintProtocol, Protocol):
    spells: Spells


@runtime_checkable
class HasStatsCup(BlueprintProtocol, Protocol):
    stats_cup: Stats


@runtime_checkable
class HasEquipmentResolved(
    HasWeapons, HasArmors, HasOtherEquipment, HasEquipmentChoices, Protocol
):
    """State after equipment choices have been resolved."""


@runtime_checkable
class HasOtherAbilities(BlueprintProtocol, Protocol):
    other_active_abilities: tuple[str, ...]


@runtime_checkable
class HasMagicalItems(BlueprintProtocol, Protocol):
    magical_items: tuple[MagicalItem, ...]


@runtime_checkable
class HasWizardLevel(HasClasses, Protocol):
    def get_wizard_level(self) -> PositiveInt: ...


@runtime_checkable
class HasSorcererLevel(HasClasses, Protocol):
    def get_sorcerer_level(self) -> PositiveInt: ...


@runtime_checkable
class HasBackstory(BlueprintProtocol, Protocol):
    backstory: str


@runtime_checkable
class HasHeight(BlueprintProtocol, Protocol):
    height: PositiveInt


@runtime_checkable
class HasWeight(BlueprintProtocol, Protocol):
    weight: PositiveInt


@runtime_checkable
class HasEyeColor(BlueprintProtocol, Protocol):
    eye_color: str


@runtime_checkable
class HasSkinColor(BlueprintProtocol, Protocol):
    skin_color: str


@runtime_checkable
class HasHairstyle(BlueprintProtocol, Protocol):
    hairstyle: str


@runtime_checkable
class HasAppearance(BlueprintProtocol, Protocol):
    appearance: str


@runtime_checkable
class HasCharacterTraits(BlueprintProtocol, Protocol):
    character_traits: str


@runtime_checkable
class HasIdeals(BlueprintProtocol, Protocol):
    ideals: str


@runtime_checkable
class HasBonds(BlueprintProtocol, Protocol):
    bonds: str


@runtime_checkable
class HasWeaknesses(BlueprintProtocol, Protocol):
    weaknesses: str


@runtime_checkable
class HasInitialData(BlueprintProtocol, Protocol):
    name: str
    sex: Sex
    age: PositiveInt
    background: Background
    alignment: Alignment
    backstory: str
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
