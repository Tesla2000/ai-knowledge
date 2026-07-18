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


class BarbarianLevel14TotemWarrior(
    BarbarianSubclassFeatureLevelBase[
        ClassSubclassLevel[
            Literal[ThirdSubclassPostLevel.THIRTEENTH], BarbarianSubclass
        ],
        ClassSubclassLevel[
            Literal[ThirdSubclassPostLevel.FOURTEENTH], BarbarianSubclass
        ],
    ]
):
    """Grants Totem Warrior level 14 subclass feature."""

    type: Literal[BuildingBlockType.BARBARIAN_LEVEL_14_TOTEM_WARRIOR] = (
        BuildingBlockType.BARBARIAN_LEVEL_14_TOTEM_WARRIOR
    )
    attunement_resolver: AnyTotemChoiceResolver = Field(
        default_factory=RandomTotemChoiceResolver
    )

    def _attunement_description(self, totem: TotemAnimal) -> str:
        descriptions = {
            TotemAnimal.BEAR: (
                "While you're raging, any creature within 5 feet of you that's hostile to "
                "you has disadvantage on attack rolls against targets other than you or "
                "another character with this feature. An enemy is immune to this effect if "
                "it can't see or hear you or if it can't be frightened."
            ),
            TotemAnimal.EAGLE: (
                "While raging, you have a flying speed equal to your current walking speed. "
                "This benefit works only in short bursts; you fall if you end your turn in "
                "the air and nothing else is holding you aloft."
            ),
            TotemAnimal.ELK: (
                "While raging, you can use a bonus action during your move to pass through "
                "the space of a Large or smaller creature. That creature must succeed on a "
                "Strength saving throw (DC 8 + your Strength bonus + your proficiency bonus) "
                "or be knocked prone and take bludgeoning damage equal to 1d12 + your "
                "Strength modifier."
            ),
            TotemAnimal.TIGER: (
                "While you're raging, if you move at least 20 feet in a straight line toward "
                "a Large or smaller target right before making a melee weapon attack against "
                "it, you can use a bonus action to make an additional melee weapon attack "
                "against it."
            ),
            TotemAnimal.WOLF: (
                "While you're raging, you can use a bonus action on your turn to knock a "
                "Large or smaller creature prone when you hit it with melee weapon attack."
            ),
        }
        return descriptions[totem]

    def _update_blueprint(self, blueprint: _BPT) -> _BPT:
        return blueprint.model_copy(
            update={
                "classes": blueprint.classes.model_copy(update={"barbarian": 14}),
                "actions": blueprint.actions + (AbilityName.TOTEMIC_ATTUNEMENT,),
            }
        )
