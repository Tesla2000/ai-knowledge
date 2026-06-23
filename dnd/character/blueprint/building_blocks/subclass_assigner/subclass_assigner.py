"""Concrete subclass assigners — one per D&D class, with Literal-typed subclass field."""

from __future__ import annotations

from typing import Literal

from typing_protocol_intersection import ProtocolIntersection

from dnd.character.blueprint.building_blocks.subclass_assigner.base import (
    SubclassAssigner,
)
from dnd.character.blueprint.state import HasClasses
from dnd.character.blueprint.state import HasSubclasses
from dnd.choices.class_creation.character_class import ArtificerSubclass
from dnd.choices.class_creation.character_class import BarbarianSubclass
from dnd.choices.class_creation.character_class import BardSubclass
from dnd.choices.class_creation.character_class import Class
from dnd.choices.class_creation.character_class import ClericSubclass
from dnd.choices.class_creation.character_class import DruidSubclass
from dnd.choices.class_creation.character_class import FighterSubclass
from dnd.choices.class_creation.character_class import MonkSubclass
from dnd.choices.class_creation.character_class import PaladinSubclass
from dnd.choices.class_creation.character_class import RangerSubclass
from dnd.choices.class_creation.character_class import RogueSubclass
from dnd.choices.class_creation.character_class import SorcererSubclass
from dnd.choices.class_creation.character_class import WarlockSubclass
from dnd.choices.class_creation.character_class import WizardSubclass
from pydantic import Field


class ArtificerSubclassAssigner[T: ProtocolIntersection[HasClasses, HasSubclasses]](
    SubclassAssigner[T]
):
    """Assigns a specific Artificer subclass to the character."""

    class_: Literal[Class.ARTIFICER] = Class.ARTIFICER
    subclass: Literal[
        ArtificerSubclass.ALCHEMIST,
        ArtificerSubclass.ARMORER,
        ArtificerSubclass.ARTILLERIST,
        ArtificerSubclass.BATTLE_SMITH,
    ] = Field(description="Artificer subclass selection")


class BarbarianSubclassAssigner[T: ProtocolIntersection[HasClasses, HasSubclasses]](
    SubclassAssigner[T]
):
    """Assigns a specific Barbarian subclass to the character."""

    class_: Literal[Class.BARBARIAN] = Class.BARBARIAN
    subclass: Literal[
        BarbarianSubclass.ANCESTRAL_GUARDIAN,
        BarbarianSubclass.BATTLERAGER,
        BarbarianSubclass.BEAST,
        BarbarianSubclass.BERSERKER,
        BarbarianSubclass.GIANT,
        BarbarianSubclass.STORM_HERALD,
        BarbarianSubclass.TOTEM_WARRIOR,
        BarbarianSubclass.WILD_MAGIC,
        BarbarianSubclass.ZEALOT,
    ] = Field(description="Barbarian subclass selection")


class BardSubclassAssigner[T: ProtocolIntersection[HasClasses, HasSubclasses]](
    SubclassAssigner[T]
):
    """Assigns a specific Bard subclass to the character."""

    class_: Literal[Class.BARD] = Class.BARD
    subclass: Literal[
        BardSubclass.CREATION,
        BardSubclass.ELOQUENCE,
        BardSubclass.GLAMOUR,
        BardSubclass.LORE,
        BardSubclass.SPIRITS,
        BardSubclass.SWORDS,
        BardSubclass.VALOR,
        BardSubclass.WHISPERS,
    ] = Field(description="Bard subclass selection")


class ClericSubclassAssigner[T: ProtocolIntersection[HasClasses, HasSubclasses]](
    SubclassAssigner[T]
):
    """Assigns a specific Cleric subclass to the character."""

    class_: Literal[Class.CLERIC] = Class.CLERIC
    subclass: Literal[
        ClericSubclass.ARCANA,
        ClericSubclass.DEATH,
        ClericSubclass.FORGE,
        ClericSubclass.GRAVE,
        ClericSubclass.KNOWLEDGE,
        ClericSubclass.LIFE,
        ClericSubclass.LIGHT,
        ClericSubclass.NATURE,
        ClericSubclass.ORDER,
        ClericSubclass.PEACE,
        ClericSubclass.TEMPEST,
        ClericSubclass.TRICKERY,
        ClericSubclass.TWILIGHT,
        ClericSubclass.WAR,
    ] = Field(description="Cleric subclass selection")


class DruidSubclassAssigner[T: ProtocolIntersection[HasClasses, HasSubclasses]](
    SubclassAssigner[T]
):
    """Assigns a specific Druid subclass to the character."""

    class_: Literal[Class.DRUID] = Class.DRUID
    subclass: Literal[
        DruidSubclass.DREAMS,
        DruidSubclass.LAND,
        DruidSubclass.MOON,
        DruidSubclass.SHEPHERD,
        DruidSubclass.SPORES,
        DruidSubclass.STARS,
        DruidSubclass.WILDFIRE,
    ] = Field(description="Druid subclass selection")


class FighterSubclassAssigner[T: ProtocolIntersection[HasClasses, HasSubclasses]](
    SubclassAssigner[T]
):
    """Assigns a specific Fighter subclass to the character."""

    class_: Literal[Class.FIGHTER] = Class.FIGHTER
    subclass: Literal[
        FighterSubclass.ARCANE_ARCHER,
        FighterSubclass.BANNERET,
        FighterSubclass.BATTLE_MASTER,
        FighterSubclass.CAVALIER,
        FighterSubclass.CHAMPION,
        FighterSubclass.ECHO_KNIGHT,
        FighterSubclass.ELDRITCH_KNIGHT,
        FighterSubclass.PSI_WARRIOR,
        FighterSubclass.RUNE_KNIGHT,
        FighterSubclass.SAMURAI,
    ] = Field(description="Fighter subclass selection")


class MonkSubclassAssigner[T: ProtocolIntersection[HasClasses, HasSubclasses]](
    SubclassAssigner[T]
):
    """Assigns a specific Monk subclass to the character."""

    class_: Literal[Class.MONK] = Class.MONK
    subclass: Literal[
        MonkSubclass.MERCY,
        MonkSubclass.ASCENDANT_DRAGON,
        MonkSubclass.ASTRAL_SELF,
        MonkSubclass.DRUNKEN_MASTER,
        MonkSubclass.FOUR_ELEMENTS,
        MonkSubclass.KENSEI,
        MonkSubclass.LONG_DEATH,
        MonkSubclass.OPEN_HAND,
        MonkSubclass.SHADOW,
        MonkSubclass.SUN_SOUL,
    ] = Field(description="Monk subclass selection")


class PaladinSubclassAssigner[T: ProtocolIntersection[HasClasses, HasSubclasses]](
    SubclassAssigner[T]
):
    """Assigns a specific Paladin subclass to the character."""

    class_: Literal[Class.PALADIN] = Class.PALADIN
    subclass: Literal[
        PaladinSubclass.ANCIENTS,
        PaladinSubclass.CONQUEST,
        PaladinSubclass.CROWN,
        PaladinSubclass.DEVOTION,
        PaladinSubclass.GLORY,
        PaladinSubclass.REDEMPTION,
        PaladinSubclass.VENGEANCE,
        PaladinSubclass.WATCHERS,
        PaladinSubclass.OATHBREAKER,
    ] = Field(description="Paladin subclass selection")


class RangerSubclassAssigner[T: ProtocolIntersection[HasClasses, HasSubclasses]](
    SubclassAssigner[T]
):
    """Assigns a specific Ranger subclass to the character."""

    class_: Literal[Class.RANGER] = Class.RANGER
    subclass: Literal[
        RangerSubclass.BEAST_MASTER,
        RangerSubclass.DRAKEWARDEN,
        RangerSubclass.FEY_WANDERER,
        RangerSubclass.GLOOM_STALKER,
        RangerSubclass.HORIZON_WALKER,
        RangerSubclass.HUNTER,
        RangerSubclass.MONSTER_SLAYER,
        RangerSubclass.SWARMKEEPER,
    ] = Field(description="Ranger subclass selection")


class RogueSubclassAssigner[T: ProtocolIntersection[HasClasses, HasSubclasses]](
    SubclassAssigner[T]
):
    """Assigns a specific Rogue subclass to the character."""

    class_: Literal[Class.ROGUE] = Class.ROGUE
    subclass: Literal[
        RogueSubclass.ARCANE_TRICKSTER,
        RogueSubclass.ASSASSIN,
        RogueSubclass.INQUISITIVE,
        RogueSubclass.MASTERMIND,
        RogueSubclass.PHANTOM,
        RogueSubclass.SCOUT,
        RogueSubclass.SOULKNIFE,
        RogueSubclass.SWASHBUCKLER,
        RogueSubclass.THIEF,
    ] = Field(description="Rogue subclass selection")


class SorcererSubclassAssigner[T: ProtocolIntersection[HasClasses, HasSubclasses]](
    SubclassAssigner[T]
):
    """Assigns a specific Sorcerer subclass to the character."""

    class_: Literal[Class.SORCERER] = Class.SORCERER
    subclass: Literal[
        SorcererSubclass.ABERRANT_MIND,
        SorcererSubclass.CLOCKWORK_SOUL,
        SorcererSubclass.DRACONIC_BLOODLINE,
        SorcererSubclass.DIVINE_SOUL,
        SorcererSubclass.LUNAR_SORCERY,
        SorcererSubclass.SHADOW_MAGIC,
        SorcererSubclass.STORM_SORCERY,
        SorcererSubclass.WILD_MAGIC,
    ] = Field(description="Sorcerer subclass selection")


class WarlockSubclassAssigner[T: ProtocolIntersection[HasClasses, HasSubclasses]](
    SubclassAssigner[T]
):
    """Assigns a specific Warlock subclass to the character."""

    class_: Literal[Class.WARLOCK] = Class.WARLOCK
    subclass: Literal[
        WarlockSubclass.ARCHFEY,
        WarlockSubclass.CELESTIAL,
        WarlockSubclass.FATHOMLESS,
        WarlockSubclass.FIEND,
        WarlockSubclass.GENIE,
        WarlockSubclass.GREAT_OLD_ONE,
        WarlockSubclass.HEXBLADE,
        WarlockSubclass.UNDEAD,
        WarlockSubclass.UNDYING,
    ] = Field(description="Warlock subclass selection")


class WizardSubclassAssigner[T: ProtocolIntersection[HasClasses, HasSubclasses]](
    SubclassAssigner[T]
):
    """Assigns a specific Wizard subclass to the character."""

    class_: Literal[Class.WIZARD] = Class.WIZARD
    subclass: Literal[
        WizardSubclass.ABJURATION,
        WizardSubclass.BLADESINGING,
        WizardSubclass.CHRONURGY,
        WizardSubclass.CONJURATION,
        WizardSubclass.DIVINATION,
        WizardSubclass.ENCHANTMENT,
        WizardSubclass.EVOCATION,
        WizardSubclass.GRAVITURGY,
        WizardSubclass.ILLUSION,
        WizardSubclass.NECROMANCY,
        WizardSubclass.SCRIBES,
        WizardSubclass.TRANSMUTATION,
        WizardSubclass.WAR_MAGIC,
    ] = Field(description="Wizard subclass selection")
