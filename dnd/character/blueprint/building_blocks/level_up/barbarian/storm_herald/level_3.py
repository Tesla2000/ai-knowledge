from typing import Literal

from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)
from dnd.character.blueprint.building_blocks.level_up.barbarian.base import (
    BarbarianSubclassAssignLevelBase,
)
from dnd.character.blueprint.states.state import _BPT
from dnd.choices.class_creation.character_class import BarbarianSubclass

from dnd.character._ability_name import AbilityName


class BarbarianLevel3StormHerald(
    BarbarianSubclassAssignLevelBase[Literal[BarbarianSubclass.STORM_HERALD]]
):
    """Assigns Path of the Storm Herald subclass at level 3."""

    type: Literal[BuildingBlockType.BARBARIAN_LEVEL_3_STORM_HERALD] = (
        BuildingBlockType.BARBARIAN_LEVEL_3_STORM_HERALD
    )

    def _update_blueprint(self, blueprint: _BPT) -> _BPT:
        return blueprint.model_copy(
            update={
                "classes": blueprint.classes.model_copy(update={"barbarian": 3}),
                "subclasses": blueprint.subclasses + (BarbarianSubclass.STORM_HERALD,),
                "actions": blueprint.actions + (AbilityName.STORM_AURA,),
            }
        )
