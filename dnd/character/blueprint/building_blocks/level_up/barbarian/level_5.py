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


class BarbarianLevel5(
    BarbarianSharedLevelBase[
        Literal[ThirdSubclassPostLevel.FOURTH],
        Literal[ThirdSubclassPostLevel.FIFTH],
    ]
):
    """Increments barbarian to level 5."""

    type: Literal[BuildingBlockType.BARBARIAN_LEVEL_5] = (
        BuildingBlockType.BARBARIAN_LEVEL_5
    )

    def _update_blueprint(self, blueprint: _BPT) -> _BPT:
        return blueprint.model_copy(
            update={
                "classes": blueprint.classes.model_copy(update={"barbarian": 5}),
                "actions": blueprint.actions
                + (AbilityName.EXTRA_ATTACK, AbilityName.FAST_MOVEMENT),
            }
        )
