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


class BarbarianLevel13(
    BarbarianSharedLevelBase[
        Literal[ThirdSubclassPostLevel.TWELFTH],
        Literal[ThirdSubclassPostLevel.THIRTEENTH],
    ]
):
    """Increments barbarian to level 13."""

    type: Literal[BuildingBlockType.BARBARIAN_LEVEL_13] = (
        BuildingBlockType.BARBARIAN_LEVEL_13
    )

    def _update_blueprint(self, blueprint: _BPT) -> _BPT:
        return blueprint.model_copy(
            update={
                "classes": blueprint.classes.model_copy(update={"barbarian": 13}),
                "actions": blueprint.actions + (AbilityName.BRUTAL_CRITICAL_2_DICE,),
            }
        )
