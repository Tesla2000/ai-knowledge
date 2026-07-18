from typing import Literal

from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)
from dnd.character.blueprint.building_blocks.level_up.barbarian.base import (
    BarbarianSubclassFeatureLevelBase,
)
from dnd.character.blueprint.sentinels import ClassSubclassLevel
from dnd.character.blueprint.sentinels import ThirdSubclassPostLevel
from dnd.choices.class_creation.character_class import BarbarianSubclass
from dnd.character.blueprint.states.state import _BPT

from dnd.character._ability_name import AbilityName


class BarbarianLevel6Beast(
    BarbarianSubclassFeatureLevelBase[
        ClassSubclassLevel[Literal[ThirdSubclassPostLevel.FIFTH], BarbarianSubclass],
        ClassSubclassLevel[Literal[ThirdSubclassPostLevel.SIXTH], BarbarianSubclass],
    ]
):
    """Grants Beast level 6 subclass feature."""

    type: Literal[BuildingBlockType.BARBARIAN_LEVEL_6_BEAST] = (
        BuildingBlockType.BARBARIAN_LEVEL_6_BEAST
    )

    def _update_blueprint(self, blueprint: _BPT) -> _BPT:
        return blueprint.model_copy(
            update={
                "classes": blueprint.classes.model_copy(update={"barbarian": 6}),
                "actions": blueprint.actions + (AbilityName.BESTIAL_SOUL,),
            }
        )
