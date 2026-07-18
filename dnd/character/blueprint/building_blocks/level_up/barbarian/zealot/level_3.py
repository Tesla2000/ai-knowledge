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


class BarbarianLevel3Zealot(
    BarbarianSubclassAssignLevelBase[Literal[BarbarianSubclass.ZEALOT]]
):
    """Assigns Path of the Zealot subclass at level 3."""

    type: Literal[BuildingBlockType.BARBARIAN_LEVEL_3_ZEALOT] = (
        BuildingBlockType.BARBARIAN_LEVEL_3_ZEALOT
    )

    def _update_blueprint(self, blueprint: _BPT) -> _BPT:
        return blueprint.model_copy(
            update={
                "classes": blueprint.classes.model_copy(update={"barbarian": 3}),
                "subclasses": blueprint.subclasses + (BarbarianSubclass.ZEALOT,),
                "actions": blueprint.actions
                + (AbilityName.DIVINE_FURY, AbilityName.WARRIOR_OF_THE_GODS),
            }
        )
