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


class SorcererLevel2(
    SorcererSharedLevelBase[
        Literal[FirstSubclassPostLevel.FIRST],
        Literal[FirstSubclassPostLevel.SECOND],
    ]
):
    """Increments sorcerer to level 2."""

    type: Literal[BuildingBlockType.SORCERER_LEVEL_2] = (
        BuildingBlockType.SORCERER_LEVEL_2
    )

    def _update_blueprint(self, blueprint: _SBPT) -> _SBPT:
        return blueprint.model_copy(
            update={
                "classes": blueprint.classes.model_copy(update={"sorcerer": 2}),
                "actions": blueprint.actions
                + (AbilityName.FONT_OF_MAGIC, AbilityName.FLEXIBLE_CASTING),
            }
        )
