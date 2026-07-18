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


class BarbarianLevel15(
    BarbarianSharedLevelBase[
        Literal[ThirdSubclassPostLevel.FOURTEENTH],
        Literal[ThirdSubclassPostLevel.FIFTEENTH],
    ]
):
    """Increments barbarian to level 15."""

    type: Literal[BuildingBlockType.BARBARIAN_LEVEL_15] = (
        BuildingBlockType.BARBARIAN_LEVEL_15
    )

    def _update_blueprint(self, blueprint: _BPT) -> _BPT:
        return blueprint.model_copy(
            update={
                "classes": blueprint.classes.model_copy(update={"barbarian": 15}),
                "actions": blueprint.actions + (AbilityName.PERSISTENT_RAGE,),
            }
        )
