from typing import Literal

from pydantic import Field

from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)
from dnd.character.blueprint.building_blocks.level_up.barbarian.base import (
    BarbarianSubclassFeatureLevelBase,
)
from dnd.character.blueprint.building_blocks.totem_choice_resolver import (
    AnyTotemChoiceResolver,
)
from dnd.character.blueprint.building_blocks.totem_choice_resolver.random import (
    RandomTotemChoiceResolver,
)
from dnd.character.blueprint.sentinels import ClassSubclassLevel
from dnd.character.blueprint.sentinels import ThirdSubclassPostLevel
from dnd.choices.class_creation.character_class import BarbarianSubclass
from dnd.character.blueprint.states.state import _BPT
from dnd.character._ability_name import AbilityName
from dnd.choices.abilities.totem_animal import TotemAnimal


class BarbarianLevel6TotemWarrior(
    BarbarianSubclassFeatureLevelBase[
        ClassSubclassLevel[Literal[ThirdSubclassPostLevel.FIFTH], BarbarianSubclass],
        ClassSubclassLevel[Literal[ThirdSubclassPostLevel.SIXTH], BarbarianSubclass],
    ]
):
    """Grants Totem Warrior level 6 subclass feature."""

    type: Literal[BuildingBlockType.BARBARIAN_LEVEL_6_TOTEM_WARRIOR] = (
        BuildingBlockType.BARBARIAN_LEVEL_6_TOTEM_WARRIOR
    )
    aspect_resolver: AnyTotemChoiceResolver = Field(
        default_factory=RandomTotemChoiceResolver
    )

    def _aspect_description(self, totem: TotemAnimal) -> str:
        descriptions = {
            TotemAnimal.BEAR: (
                "You gain the might of a bear. Your carrying capacity (including maximum "
                "load and maximum lift) is doubled, and you have advantage on Strength "
                "checks made to push, pull, lift, or break things."
            ),
            TotemAnimal.EAGLE: (
                "You gain the eyesight of an eagle. You can see up to 1 mile away with no "
                "difficulty, able to discern even fine details as though looking at something "
                "no more than 100 feet away from you. Additionally, dim light doesn't impose "
                "disadvantage on your Wisdom (Perception) checks."
            ),
            TotemAnimal.ELK: (
                "Whether mounted or on foot, your travel pace is doubled, as is the travel "
                "pace of up to ten companions while they're within 60 feet of you and you're "
                "not incapacitated. The elk spirit helps you roam far and fast."
            ),
            TotemAnimal.TIGER: (
                "You gain proficiency in two skills from the following list: Athletics, "
                "Acrobatics, Stealth, and Survival. The cat spirit hones your survival instincts."
            ),
            TotemAnimal.WOLF: (
                "You gain the hunting sensibilities of a wolf. You can track other creatures "
                "while traveling at a fast pace, and you can move stealthily while traveling "
                "at a normal pace."
            ),
        }
        return descriptions[totem]

    def _update_blueprint(self, blueprint: _BPT) -> _BPT:
        return blueprint.model_copy(
            update={
                "classes": blueprint.classes.model_copy(update={"barbarian": 6}),
                "actions": blueprint.actions + (AbilityName.ASPECT_OF_THE_BEAST,),
            }
        )
