from typing import ClassVar
from typing import Generic
from typing import Literal
from typing import TypeAlias
from typing import TypeVar
from typing import cast

from dnd.character.armor.names import ArmorName
from dnd.character.magical_item.item import MagicalItem
from dnd.character.blueprint.sentinels import Level
from dnd.character.feature.feats import FeatName
from dnd.character.race.subraces import SubraceName
from dnd.character.spells.spells import Spells
from dnd.character.stats import Stats
from dnd.choices.class_creation.character_class import AnySubclass
from dnd.choices.equipment_creation.weapons import WeaponName
from dnd.choices.language import Language
from dnd.choices.stats_creation.statistic import Statistic
from dnd.other_profficiencies import ArmorProficiency
from dnd.other_profficiencies import GamingSet
from dnd.other_profficiencies import MusicalInstrument
from dnd.other_profficiencies import ToolProficiency
from dnd.other_profficiencies import WeaponProficiency
from dnd.skill_proficiency import Skill
from dnd.character.class_levels import ClassLevels
from dnd.choices.abilities.action import AnyAction
from pydantic import Field
from pydantic import NonNegativeInt, BaseModel, ConfigDict
from pydantic import PositiveInt
from dnd.character.blueprint.sentinels import ClassPreSubclassLevel
from dnd.character.blueprint.sentinels import FirstSubclassPreLevel
from dnd.character.blueprint.sentinels import SecondSubclassPreLevel
from dnd.character.blueprint.sentinels import SorcererPreSubclassLevel
from dnd.character.blueprint.sentinels import ThirdSubclassPreLevel
from dnd.character.blueprint.sentinels import WizardPreSubclassLevel
from dnd.character.blueprint.sentinels import _ARK_co
from dnd.character.blueprint.sentinels import _BAK_co
from dnd.character.blueprint.sentinels import _BDK_co
from dnd.character.blueprint.sentinels import _CDK_co
from dnd.character.blueprint.sentinels import _CLK_co
from dnd.character.blueprint.sentinels import _DRK_co
from dnd.character.blueprint.sentinels import _FGK_co
from dnd.character.blueprint.sentinels import _HeK_co
from dnd.character.blueprint.sentinels import _MOK_co
from dnd.character.blueprint.sentinels import _PAK_co
from dnd.character.blueprint.sentinels import _RAK_co
from dnd.character.blueprint.sentinels import _RK_co
from dnd.character.blueprint.sentinels import _ROK_co
from dnd.character.blueprint.sentinels import _SOK_co
from dnd.character.blueprint.sentinels import _SkCK_co
from dnd.character.blueprint.sentinels import _StCK_co
from dnd.character.blueprint.sentinels import _StK_co
from dnd.character.blueprint.sentinels import _WAK_co
from dnd.character.blueprint.sentinels import _WZK_co
from dnd.character.blueprint.sentinels import AnyClassLevel
from dnd.character.blueprint.sentinels import AnySorcererLevel
from dnd.character.blueprint.sentinels import AnyStatChoices
from dnd.character.blueprint.sentinels import AnyWizardLevel
from dnd.character.blueprint.sentinels import MaybeCharacterData
from dnd.character.blueprint.sentinels import MaybeHealth
from dnd.character.blueprint.sentinels import MaybeRace
from dnd.character.blueprint.sentinels import MaybeStats

type Equipment = WeaponName | ArmorName | str


class Blueprint(
    BaseModel,
    Generic[
        _RK_co,
        _StK_co,
        _HeK_co,
        _StCK_co,
        _SkCK_co,
        _WZK_co,
        _SOK_co,
        _FGK_co,
        _BAK_co,
        _ROK_co,
        _CLK_co,
        _DRK_co,
        _PAK_co,
        _RAK_co,
        _MOK_co,
        _BDK_co,
        _WAK_co,
        _ARK_co,
        _CDK_co,
    ],
):
    """Flat character state. Type params encode what's been set:
    _RK=Race means race is set; _HeK=PositiveInt means health is set;
    _WZK=WizardSubclassLevel[...] means wizard subclass is assigned; etc.
    Building blocks transform Blueprint[InKey] -> Blueprint[OutKey].
    """

    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    race: _RK_co = Field(default=cast(_RK_co, None))
    subrace: SubraceName | None = None
    speed: PositiveInt | None = None
    dark_vision_range: NonNegativeInt | None = None
    stats: _StK_co = Field(default=cast(_StK_co, None))
    health_base: _HeK_co = Field(default=cast(_HeK_co, None))

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
    actions: tuple[AnyAction, ...] = Field(default=())
    n_stat_choices: _StCK_co = Field(default=cast(_StCK_co, 0))
    n_skill_choices: _SkCK_co = Field(default=cast(_SkCK_co, 0))
    skills_to_choose_from: frozenset[Skill] = Field(default_factory=frozenset)
    equipment_choices: tuple[tuple[Equipment, ...], ...] = ()
    level: Level | None = None
    character_data: _CDK_co = Field(default=cast(_CDK_co, None))


_Z = Literal[SecondSubclassPreLevel.ZEROTH]
_SZ = Literal[FirstSubclassPreLevel.ZEROTH]
_TZ = Literal[ThirdSubclassPreLevel.ZEROTH]

EmptyBlueprint: TypeAlias = Blueprint[
    None,
    None,
    None,
    Literal[0],
    Literal[0],
    WizardPreSubclassLevel[_Z, None],
    SorcererPreSubclassLevel[_SZ, None],
    ClassPreSubclassLevel[_TZ, None],
    ClassPreSubclassLevel[_TZ, None],
    ClassPreSubclassLevel[_TZ, None],
    ClassPreSubclassLevel[_TZ, None],
    ClassPreSubclassLevel[_TZ, None],
    ClassPreSubclassLevel[_TZ, None],
    ClassPreSubclassLevel[_TZ, None],
    ClassPreSubclassLevel[_TZ, None],
    ClassPreSubclassLevel[_TZ, None],
    ClassPreSubclassLevel[_TZ, None],
    ClassPreSubclassLevel[_TZ, None],
    None,
]
type AnyBluprint = Blueprint[
    MaybeRace,
    MaybeStats,
    MaybeHealth,
    AnyStatChoices,
    AnyStatChoices,
    AnyWizardLevel,
    AnySorcererLevel,
    AnyClassLevel,
    AnyClassLevel,
    AnyClassLevel,
    AnyClassLevel,
    AnyClassLevel,
    AnyClassLevel,
    AnyClassLevel,
    AnyClassLevel,
    AnyClassLevel,
    AnyClassLevel,
    AnyClassLevel,
    MaybeCharacterData,
]
_BPT = TypeVar("_BPT", bound=AnyBluprint)
