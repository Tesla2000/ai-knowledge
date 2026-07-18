from typing import Literal

from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)
from dnd.character.blueprint.building_blocks.level_up.barbarian.base import (
    BarbarianPreSubclassLevelBase,
)
from dnd.character.blueprint.sentinels import ThirdSubclassPreLevel
from dnd.character.blueprint.states.state import _BPT

from dnd.character._ability_name import AbilityName


class BarbarianLevel2(
    BarbarianPreSubclassLevelBase[
        Literal[ThirdSubclassPreLevel.FIRST],
        Literal[ThirdSubclassPreLevel.SECOND],
    ]
):
    """Increments barbarian to level 2."""

    type: Literal[BuildingBlockType.BARBARIAN_LEVEL_2] = (
        BuildingBlockType.BARBARIAN_LEVEL_2
    )

    def _update_blueprint(self, blueprint: _BPT) -> _BPT:
        return blueprint.model_copy(
            update={
                "classes": blueprint.classes.model_copy(update={"barbarian": 2}),
                "actions": blueprint.actions
                + (AbilityName.RECKLESS_ATTACK, AbilityName.DANGER_SENSE),
            }
        )
