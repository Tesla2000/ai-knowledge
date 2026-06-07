from __future__ import annotations

from enum import StrEnum
from typing import Union

from frozendict import frozendict


class _Subclass(StrEnum):
    pass


class ArtificerSubclass(_Subclass):
    ALCHEMIST = "Alchemist"
    ARMORER = "Armorer"
    ARTILLERIST = "Artillerist"
    BATTLE_SMITH = "Battle Smith"


class BarbarianSubclass(_Subclass):
    ANCESTRAL_GUARDIAN = "Path of the Ancestral Guardian"
    BATTLERAGER = "Path of the Battlerager"
    BEAST = "Path of the Beast"
    BERSERKER = "Path of the Berserker"
    GIANT = "Path of the Giant"
    STORM_HERALD = "Path of the Storm Herald"
    TOTEM_WARRIOR = "Path of the Totem Warrior"
    WILD_MAGIC = "Path of Wild Magic"
    ZEALOT = "Path of the Zealot"


class BardSubclass(_Subclass):
    CREATION = "College of Creation"
    ELOQUENCE = "College of Eloquence"
    GLAMOUR = "College of Glamour"
    LORE = "College of Lore"
    SPIRITS = "College of Spirits"
    SWORDS = "College of Swords"
    VALOR = "College of Valor"
    WHISPERS = "College of Whispers"


class ClericSubclass(_Subclass):
    ARCANA = "Arcana Domain"
    DEATH = "Death Domain"
    FORGE = "Forge Domain"
    GRAVE = "Grave Domain"
    KNOWLEDGE = "Knowledge Domain"
    LIFE = "Life Domain"
    LIGHT = "Light Domain"
    NATURE = "Nature Domain"
    ORDER = "Order Domain"
    PEACE = "Peace Domain"
    TEMPEST = "Tempest Domain"
    TRICKERY = "Trickery Domain"
    TWILIGHT = "Twilight Domain"
    WAR = "War Domain"


class DruidSubclass(_Subclass):
    DREAMS = "Circle of Dreams"
    LAND = "Circle of the Land"
    MOON = "Circle of the Moon"
    SHEPHERD = "Circle of the Shepherd"
    SPORES = "Circle of Spores"
    STARS = "Circle of Stars"
    WILDFIRE = "Circle of Wildfire"


class FighterSubclass(_Subclass):
    ARCANE_ARCHER = "Arcane Archer"
    BANNERET = "Banneret"
    BATTLE_MASTER = "Battle Master"
    CAVALIER = "Cavalier"
    CHAMPION = "Champion"
    ECHO_KNIGHT = "Echo Knight"
    ELDRITCH_KNIGHT = "Eldritch Knight"
    PSI_WARRIOR = "Psi Warrior"
    RUNE_KNIGHT = "Rune Knight"
    SAMURAI = "Samurai"


class MonkSubclass(_Subclass):
    MERCY = "Way of Mercy"
    ASCENDANT_DRAGON = "Way of the Ascendant Dragon"
    ASTRAL_SELF = "Way of the Astral Self"
    DRUNKEN_MASTER = "Way of the Drunken Master"
    FOUR_ELEMENTS = "Way of the Four Elements"
    KENSEI = "Way of the Kensei"
    LONG_DEATH = "Way of the Long Death"
    OPEN_HAND = "Way of the Open Hand"
    SHADOW = "Way of Shadow"
    SUN_SOUL = "Way of the Sun Soul"


class PaladinSubclass(_Subclass):
    ANCIENTS = "Oath of the Ancients"
    CONQUEST = "Oath of Conquest"
    CROWN = "Oath of the Crown"
    DEVOTION = "Oath of Devotion"
    GLORY = "Oath of Glory"
    REDEMPTION = "Oath of Redemption"
    VENGEANCE = "Oath of Vengeance"
    WATCHERS = "Oath of the Watchers"
    OATHBREAKER = "Oathbreaker"


class RangerSubclass(_Subclass):
    BEAST_MASTER = "Beast Master Conclave"
    DRAKEWARDEN = "Drakewarden"
    FEY_WANDERER = "Fey Wanderer"
    GLOOM_STALKER = "Gloom Stalker Conclave"
    HORIZON_WALKER = "Horizon Walker Conclave"
    HUNTER = "Hunter Conclave"
    MONSTER_SLAYER = "Monster Slayer Conclave"
    SWARMKEEPER = "Swarmkeeper"


class RogueSubclass(_Subclass):
    ARCANE_TRICKSTER = "Arcane Trickster"
    ASSASSIN = "Assassin"
    INQUISITIVE = "Inquisitive"
    MASTERMIND = "Mastermind"
    PHANTOM = "Phantom"
    SCOUT = "Scout"
    SOULKNIFE = "Soulknife"
    SWASHBUCKLER = "Swashbuckler"
    THIEF = "Thief"


class SorcererSubclass(_Subclass):
    ABERRANT_MIND = "Aberrant Mind"
    CLOCKWORK_SOUL = "Clockwork Soul"
    DRACONIC_BLOODLINE = "Draconic Bloodline"
    DIVINE_SOUL = "Divine Soul"
    LUNAR_SORCERY = "Lunar Sorcery"
    SHADOW_MAGIC = "Shadow Magic"
    STORM_SORCERY = "Storm Sorcery"
    WILD_MAGIC = "Wild Magic"


class WarlockSubclass(_Subclass):
    ARCHFEY = "Archfey"
    CELESTIAL = "Celestial"
    FATHOMLESS = "Fathomless"
    FIEND = "Fiend"
    GENIE = "The Genie"
    GREAT_OLD_ONE = "Great Old One"
    HEXBLADE = "Hexblade"
    UNDEAD = "Undead"
    UNDYING = "Undying"


class WizardSubclass(_Subclass):
    ABJURATION = "School of Abjuration"
    BLADESINGING = "School of Bladesinging"
    CHRONURGY = "School of Chronurgy"
    CONJURATION = "School of Conjuration"
    DIVINATION = "School of Divination"
    ENCHANTMENT = "School of Enchantment"
    EVOCATION = "School of Evocation"
    GRAVITURGY = "School of Graviturgy"
    ILLUSION = "School of Illusion"
    NECROMANCY = "School of Necromancy"
    SCRIBES = "Order of Scribes"
    TRANSMUTATION = "School of Transmutation"
    WAR_MAGIC = "School of War Magic"


class Class(StrEnum):
    BARBARIAN = "Barbarian"
    BARD = "Bard"
    CLERIC = "Cleric"
    DRUID = "Druid"
    FIGHTER = "Fighter"
    MONK = "Monk"
    PALADIN = "Paladin"
    RANGER = "Ranger"
    ROGUE = "Rogue"
    SORCERER = "Sorcerer"
    WARLOCK = "Warlock"
    WIZARD = "Wizard"
    ARTIFICER = "Artificer"


SUBCLASSES: frozendict[Class, type[_Subclass]] = frozendict(
    {
        Class.ARTIFICER: ArtificerSubclass,
        Class.BARD: BardSubclass,
        Class.BARBARIAN: BarbarianSubclass,
        Class.CLERIC: ClericSubclass,
        Class.DRUID: DruidSubclass,
        Class.FIGHTER: FighterSubclass,
        Class.MONK: MonkSubclass,
        Class.PALADIN: PaladinSubclass,
        Class.RANGER: RangerSubclass,
        Class.ROGUE: RogueSubclass,
        Class.SORCERER: SorcererSubclass,
        Class.WARLOCK: WarlockSubclass,
        Class.WIZARD: WizardSubclass,
    }
)
AnySubclass = Union[
    ArtificerSubclass,
    BardSubclass,
    BarbarianSubclass,
    ClericSubclass,
    DruidSubclass,
    FighterSubclass,
    MonkSubclass,
    PaladinSubclass,
    RangerSubclass,
    RogueSubclass,
    SorcererSubclass,
    WarlockSubclass,
    WizardSubclass,
]

# Subclass level requirements by class
subclass_level = frozendict(
    {class_: 2 if class_ in (Class.WIZARD,) else 3 for class_ in Class}
)
if not all(map(subclass_level.__contains__, Class)):
    raise ValueError("Not all classes have assigned subclass levels")
