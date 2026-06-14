from __future__ import annotations

from enum import StrEnum
from typing import TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:
    from dnd.character_wrapper import CharacterWrapper
from dnd.choices.class_creation.character_class import (
    Class,
)


class WarlockPact(StrEnum):
    PACT_OF_THE_TOME = "Tome"
    PACT_OF_THE_TALISMAN = "Talisman"
    PACT_OF_THE_CHAIN = "Chain"
    PACT_OF_THE_BLADE = "Blade"


class EldritchInvocation(BaseModel):
    name: str
    description: str
    required_level: int
    pact: WarlockPact | None


invocations: list[EldritchInvocation] = [
    EldritchInvocation(
        name="Agonizing Blast",
        description="When you cast eldritch blast, add your Charisma modifier "
        "to the damage it deals on a hit.",
        required_level=0,
        pact=None,
    ),
    EldritchInvocation(
        name="Armor of Shadows",
        description="You can cast mage armor on yourself at will, without "
        "expending a spell slot or material components.",
        required_level=0,
        pact=None,
    ),
    EldritchInvocation(
        name="Ascendant Step",
        description="You can cast levitate on yourself at will, without "
        "expending a spell slot or material components.",
        required_level=9,
        pact=None,
    ),
    EldritchInvocation(
        name="Aspect of the Moon",
        description="You no longer need to sleep and can't be forced to sleep "
        "by any means. To gain the benefits of a long rest, you "
        "can spend all 8 hours doing light activity.",
        required_level=0,
        pact=WarlockPact.PACT_OF_THE_TOME,
    ),
    EldritchInvocation(
        name="Beast Speech",
        description="You can cast speak with animals at will, without "
        "expending a spell slot.",
        required_level=0,
        pact=None,
    ),
    EldritchInvocation(
        name="Beguiling Influence",
        description="You gain proficiency in the Deception and Persuasion skills.",
        required_level=0,
        pact=None,
    ),
    EldritchInvocation(
        name="Bewitching Whispers",
        description="You can cast compulsion once using a warlock spell slot."
        " You can't do so again until you finish a long rest.",
        required_level=7,
        pact=None,
    ),
    EldritchInvocation(
        name="Bond of the Talisman",
        description="While someone else is wearing your talisman, you can use"
        " your action to teleport to the unoccupied space closest"
        " to them.",
        required_level=12,
        pact=WarlockPact.PACT_OF_THE_TALISMAN,
    ),
    EldritchInvocation(
        name="Book of Ancient Secrets",
        description="You can now inscribe magical rituals in your Book of "
        "Shadows. Choose two 1st-level spells that have the ritual"
        " tag from any class's spell list.",
        required_level=0,
        pact=WarlockPact.PACT_OF_THE_TOME,
    ),
    EldritchInvocation(
        name="Chains of Carceri",
        description="You can cast hold monster at will – targeting a "
        "celestial, fiend, or elemental – without expending a "
        "spell slot or material components.",
        required_level=15,
        pact=WarlockPact.PACT_OF_THE_CHAIN,
    ),
    EldritchInvocation(
        name="Cloak of Flies",
        description="You can surround yourself with a magical aura that "
        "looks like buzzing flies. The aura extends 5 feet from "
        "you in every direction.",
        required_level=5,
        pact=None,
    ),
    EldritchInvocation(
        name="Devil's Sight",
        description="You can see normally in darkness, both magical and "
        "nonmagical, to a distance of 120 feet.",
        required_level=0,
        pact=None,
    ),
    EldritchInvocation(
        name="Dreadful Word",
        description="You can cast confusion once using a warlock spell slot. "
        "You can't do so again until you finish a long rest.",
        required_level=7,
        pact=None,
    ),
    EldritchInvocation(
        name="Eldritch Mind",
        description="You have advantage on Constitution saving throws that "
        "you make to maintain your concentration on a spell.",
        required_level=0,
        pact=None,
    ),
    EldritchInvocation(
        name="Eldritch Sight",
        description="You can cast detect magic at will, without expending a "
        "spell slot or material components.",
        required_level=0,
        pact=None,
    ),
    EldritchInvocation(
        name="Eldritch Smite",
        description="Once per turn when you hit a creature with your pact "
        "weapon, you can expend a warlock spell slot to deal "
        "extra force damage and knock the target prone.",
        required_level=5,
        pact=WarlockPact.PACT_OF_THE_BLADE,
    ),
    EldritchInvocation(
        name="Eldritch Spear",
        description="When you cast eldritch blast, its range is 300 feet.",
        required_level=0,
        pact=None,
    ),
    EldritchInvocation(
        name="Eyes of the Rune Keeper",
        description="You can read all writing.",
        required_level=0,
        pact=None,
    ),
    EldritchInvocation(
        name="Far Scribe",
        description="A new page appears in your Book of Shadows for casting "
        "sending without using a spell slot or components.",
        required_level=5,
        pact=WarlockPact.PACT_OF_THE_TOME,
    ),
    EldritchInvocation(
        name="Fiendish Vigor",
        description="You can cast false life on yourself at will as a 1st-level spell.",
        required_level=0,
        pact=None,
    ),
    EldritchInvocation(
        name="Gaze of Two Minds",
        description="You can perceive through the senses of a willing humanoid.",
        required_level=0,
        pact=None,
    ),
    EldritchInvocation(
        name="Ghostly Gaze",
        description="You can see through solid objects to a range of 30 feet, "
        "gaining darkvision if you don't have it.",
        required_level=7,
        pact=None,
    ),
    EldritchInvocation(
        name="Gift of the Depths",
        description="You can breathe underwater, gain a swimming speed, and "
        "cast water breathing once per long rest.",
        required_level=5,
        pact=None,
    ),
    EldritchInvocation(
        name="Gift of the Ever-Living Ones",
        description="Whenever you regain hit points while your familiar is "
        "within 100 feet of you, treat dice rolled for hit points as maximum.",
        required_level=0,
        pact=WarlockPact.PACT_OF_THE_CHAIN,
    ),
    EldritchInvocation(
        name="Gift of the Protectors",
        description="When a creature whose name is in your Book of Shadows "
        "drops to 0 hit points, it drops to 1 hit point instead.",
        required_level=9,
        pact=WarlockPact.PACT_OF_THE_TOME,
    ),
    EldritchInvocation(
        name="Grasp of Hadar",
        description="Once per turn when you hit a creature with eldritch "
        "blast, you can move the creature 10 feet closer to "
        "yourself.",
        required_level=0,
        pact=None,
    ),
    EldritchInvocation(
        name="Improved Pact Weapon",
        description="You can use any weapon you summon with your Pact of the "
        "Blade feature as a spellcasting focus and gain a +1 "
        "bonus to attack and damage rolls.",
        required_level=0,
        pact=WarlockPact.PACT_OF_THE_BLADE,
    ),
    EldritchInvocation(
        name="Investment of the Chain Master",
        description="When you cast find familiar, the familiar gains various "
        "benefits and you can use your reaction to grant it "
        "resistance against damage.",
        required_level=0,
        pact=WarlockPact.PACT_OF_THE_CHAIN,
    ),
    EldritchInvocation(
        name="Lance of Lethargy",
        description="Once per turn when you hit a creature with eldritch "
        "blast, you can reduce its speed by 10 feet until the end of your "
        "next turn.",
        required_level=0,
        pact=None,
    ),
    EldritchInvocation(
        name="Lifedrinker",
        description="When you hit a creature with your pact weapon, it takes"
        " extra necrotic damage equal to your Charisma modifier.",
        required_level=12,
        pact=WarlockPact.PACT_OF_THE_BLADE,
    ),
    EldritchInvocation(
        name="Maddening Hex",
        description="You cause a psychic disturbance around the target cursed "
        "by your hex spell or a warlock feature, dealing psychic "
        "damage to the target and nearby creatures.",
        required_level=5,
        pact=None,
    ),
    EldritchInvocation(
        name="Mask of Many Faces",
        description="You can cast disguise self at will, without expending a "
        "spell slot.",
        required_level=0,
        pact=None,
    ),
    EldritchInvocation(
        name="Master of Myriad Forms",
        description="You can cast alter self at will, without expending a spell slot.",
        required_level=15,
        pact=None,
    ),
    EldritchInvocation(
        name="Minions of Chaos",
        description="You can cast conjure elemental once using a warlock spell"
        " slot. You can't do so again until you finish a long "
        "rest.",
        required_level=9,
        pact=None,
    ),
    EldritchInvocation(
        name="Misty Visions",
        description="You can cast silent image at will, without expending a "
        "spell slot or material components.",
        required_level=0,
        pact=None,
    ),
    EldritchInvocation(
        name="One with Shadows",
        description="You can use your action to become invisible in dim light "
        "or darkness for 1 hour or until you take an action.",
        required_level=5,
        pact=None,
    ),
    EldritchInvocation(
        name="Otherworldly Leap",
        description="You can cast jump on yourself at will, without expending "
        "a spell slot or material components.",
        required_level=5,
        pact=None,
    ),
    EldritchInvocation(
        name="Repelling Blast",
        description="When you hit a creature with eldritch blast, you can "
        "push it 10 feet away from you.",
        required_level=0,
        pact=None,
    ),
    EldritchInvocation(
        name="Sculptor of Flesh",
        description="You can cast alter self at will, without expending a "
        "spell slot or material components.",
        required_level=12,
        pact=None,
    ),
    EldritchInvocation(
        name="Shadow of Moil",
        description="You can cast shadow of moil once using a warlock spell "
        "slot. You can't do so again until you finish a long "
        "rest.",
        required_level=12,
        pact=None,
    ),
    EldritchInvocation(
        name="Sign of Ill Omen",
        description="You can cast bestow curse once using a warlock spell "
        "slot. You can't do so again until you finish a long "
        "rest.",
        required_level=7,
        pact=None,
    ),
    EldritchInvocation(
        name="Sculptor of Flesh",
        description="You can cast alter self at will, without expending a spell slot.",
        required_level=12,
        pact=None,
    ),
    EldritchInvocation(
        name="Thirsting Blade",
        description="You can attack twice, instead of once, when you take the "
        "Attack action with your pact weapon.",
        required_level=5,
        pact=WarlockPact.PACT_OF_THE_BLADE,
    ),
    EldritchInvocation(
        name="Tomb of Levistus",
        description="You can cast ice knife once using a warlock spell slot. "
        "You can't do so again until you finish a long rest.",
        required_level=5,
        pact=None,
    ),
    EldritchInvocation(
        name="Visions of Distant Realms",
        description="You can cast arcane eye once using a warlock spell slot. "
        "You can't do so again until you finish a long rest.",
        required_level=15,
        pact=None,
    ),
    EldritchInvocation(
        name="Witch Sight",
        description="You can see the true form of any shapechanger or creature"
        " concealed by illusion or transmutation magic.",
        required_level=15,
        pact=None,
    ),
    EldritchInvocation(
        name="Word of Changing",
        description="You can cast alter self once using a warlock spell slot. "
        "You can't do so again until you finish a long rest.",
        required_level=5,
        pact=None,
    ),
]


def n_eldrich_invocations(character_wrapper: CharacterWrapper) -> int:
    conditions = [
        lambda character_wrapper: (
            character_wrapper.character.classes == Class.WARLOCK
            and character_wrapper.character.level >= 2
        ),
        lambda character_wrapper: (
            character_wrapper.character.classes == Class.WARLOCK
            and character_wrapper.character.level >= 2
        ),
        lambda character_wrapper: (
            character_wrapper.character.classes == Class.WARLOCK
            and character_wrapper.character.level >= 5
        ),
        lambda character_wrapper: (
            character_wrapper.character.classes == Class.WARLOCK
            and character_wrapper.character.level >= 7
        ),
        lambda character_wrapper: (
            character_wrapper.character.classes == Class.WARLOCK
            and character_wrapper.character.level >= 9
        ),
        lambda character_wrapper: (
            character_wrapper.character.classes == Class.WARLOCK
            and character_wrapper.character.level >= 12
        ),
        lambda character_wrapper: (
            character_wrapper.character.classes == Class.WARLOCK
            and character_wrapper.character.level >= 15
        ),
        lambda character_wrapper: (
            character_wrapper.character.classes == Class.WARLOCK
            and character_wrapper.character.level >= 18
        ),
    ]
    return sum(condition(character_wrapper) for condition in conditions)
