from typing import Literal

from pydantic import Field

from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)
from dnd.character.blueprint.building_blocks.level_up.barbarian.base import (
    BarbarianSubclassAssignLevelBase,
)
from dnd.character.blueprint.building_blocks.totem_choice_resolver import (
    AnyTotemChoiceResolver,
)
from dnd.character.blueprint.building_blocks.totem_choice_resolver.random import (
    RandomTotemChoiceResolver,
)
from dnd.character.blueprint.states.state import _BPT
from dnd.character._ability_name import AbilityName
from dnd.choices.abilities.totem_animal import TotemAnimal
from dnd.choices.class_creation.character_class import BarbarianSubclass


class BarbarianLevel3TotemWarrior(
    BarbarianSubclassAssignLevelBase[Literal[BarbarianSubclass.TOTEM_WARRIOR]]
):
    """Assigns Path of the Totem Warrior subclass at level 3."""

    type: Literal[BuildingBlockType.BARBARIAN_LEVEL_3_TOTEM_WARRIOR] = (
        BuildingBlockType.BARBARIAN_LEVEL_3_TOTEM_WARRIOR
    )
    totem_spirit_resolver: AnyTotemChoiceResolver = Field(
        default_factory=RandomTotemChoiceResolver
    )

    def _totem_spirit_description(self, totem: TotemAnimal) -> str:
        descriptions = {
            TotemAnimal.BEAR: (
                "While raging, you have resistance to all damage except psychic damage. "
                "The spirit of the bear makes you tough enough to stand up to any punishment."
            ),
            TotemAnimal.EAGLE: (
                "While raging, other creatures have disadvantage on opportunity attack rolls "
                "against you, and you can use the Dash action as a bonus action on your turn. "
                "The spirit of the eagle makes you into a predator who can weave through the "
                "fray with ease."
            ),
            TotemAnimal.ELK: (
                "While raging, your speed increases by 15 feet. The spirit of the elk makes "
                "you extraordinarily swift."
            ),
            TotemAnimal.TIGER: (
                "While raging, you can add 10 feet to your long jump distance and 3 feet to "
                "your high jump distance. The spirit of the tiger empowers your leaps."
            ),
            TotemAnimal.WOLF: (
                "While raging, your allies have advantage on melee attack rolls against any "
                "creature within 5 feet of you that is hostile to you. The spirit of the wolf "
                "makes you a leader of hunters."
            ),
        }
        return descriptions[totem]

    def _update_blueprint(self, blueprint: _BPT) -> _BPT:
        return blueprint.model_copy(
            update={
                "classes": blueprint.classes.model_copy(update={"barbarian": 3}),
                "subclasses": blueprint.subclasses + (BarbarianSubclass.TOTEM_WARRIOR,),
                "actions": blueprint.actions
                + (AbilityName.SPIRIT_SEEKER, AbilityName.TOTEM_SPIRIT),
            }
        )
