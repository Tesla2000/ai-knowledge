from typing import Literal

from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)
from dnd.character.blueprint.building_blocks.level_up.barbarian.base import (
    BarbarianSubclassAssignLevelBase,
)
from dnd.character.blueprint.states.state import _BPT
from dnd.character._ability_name import AbilityName
from dnd.choices.class_creation.character_class import BarbarianSubclass


class BarbarianLevel3Giant(
    BarbarianSubclassAssignLevelBase[Literal[BarbarianSubclass.GIANT]]
):
    """Assigns Path of the Giant subclass at level 3."""

    type: Literal[BuildingBlockType.BARBARIAN_LEVEL_3_GIANT] = (
        BuildingBlockType.BARBARIAN_LEVEL_3_GIANT
    )

    def _update_blueprint(self, blueprint: _BPT) -> _BPT:
        return blueprint.model_copy(
            update={
                "classes": blueprint.classes.model_copy(update={"barbarian": 3}),
                "subclasses": blueprint.subclasses + (BarbarianSubclass.GIANT,),
                "actions": blueprint.actions
                + (AbilityName.GIANTS_POWER, AbilityName.GIANTS_HAVOC),
            }
        )
