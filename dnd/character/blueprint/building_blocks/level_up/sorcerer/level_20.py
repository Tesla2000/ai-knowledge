from typing import Literal

from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.base import (
    SorcererSharedLevelBase,
)
from dnd.character.blueprint.sentinels import FirstSubclassPostLevel
from dnd.character.blueprint.states.sorcerer.base import _SBPT

from dnd.character._ability_name import AbilityName


class SorcererLevel20(
    SorcererSharedLevelBase[
        Literal[FirstSubclassPostLevel.NINETEENTH],
        Literal[FirstSubclassPostLevel.TWENTIETH],
    ]
):
    """Increments sorcerer to level 20."""

    type: Literal[BuildingBlockType.SORCERER_LEVEL_20] = (
        BuildingBlockType.SORCERER_LEVEL_20
    )

    def _update_blueprint(self, blueprint: _SBPT) -> _SBPT:
        return blueprint.model_copy(
            update={
                "classes": blueprint.classes.model_copy(update={"sorcerer": 20}),
                "actions": blueprint.actions + (AbilityName.SORCEROUS_RESTORATION,),
            }
        )
