from typing import Literal

from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)
from dnd.character.blueprint.building_blocks.level_up.barbarian.base import (
    BarbarianSharedLevelBase,
)
from dnd.character.blueprint.sentinels import ThirdSubclassPostLevel
from dnd.character.blueprint.states.state import _BPT

from dnd.character._ability_name import AbilityName


class BarbarianLevel17(
    BarbarianSharedLevelBase[
        Literal[ThirdSubclassPostLevel.SIXTEENTH],
        Literal[ThirdSubclassPostLevel.SEVENTEENTH],
    ]
):
    """Increments barbarian to level 17."""

    type: Literal[BuildingBlockType.BARBARIAN_LEVEL_17] = (
        BuildingBlockType.BARBARIAN_LEVEL_17
    )

    def _update_blueprint(self, blueprint: _BPT) -> _BPT:
        return blueprint.model_copy(
            update={
                "classes": blueprint.classes.model_copy(update={"barbarian": 17}),
                "actions": blueprint.actions + (AbilityName.BRUTAL_CRITICAL_3_DICE,),
            }
        )
