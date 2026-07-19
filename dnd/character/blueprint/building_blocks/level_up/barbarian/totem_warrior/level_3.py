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

    def _update_blueprint(self, blueprint: _BPT) -> _BPT:
        return blueprint.model_copy(
            update={
                "classes": blueprint.classes.model_copy(update={"barbarian": 3}),
                "subclasses": blueprint.subclasses + (BarbarianSubclass.TOTEM_WARRIOR,),
                "actions": blueprint.actions
                + (AbilityName.SPIRIT_SEEKER, AbilityName.TOTEM_SPIRIT),
            }
        )
