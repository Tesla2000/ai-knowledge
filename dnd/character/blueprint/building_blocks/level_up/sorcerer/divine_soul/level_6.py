from typing import Literal

from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.base import (
    SorcererSubclassFeatureLevelBase,
)
from dnd.character.blueprint.sentinels import FirstSubclassPostLevel
from dnd.character.blueprint.sentinels import SorcererSubclassLevel
from dnd.character.blueprint.states.state import _BPT
from dnd.choices.class_creation.character_class import SorcererSubclass

from dnd.character._ability_name import AbilityName


class SorcererLevel6DivineSoul(
    SorcererSubclassFeatureLevelBase[
        SorcererSubclassLevel[
            Literal[FirstSubclassPostLevel.FIFTH], Literal[SorcererSubclass.DIVINE_SOUL]
        ],
        SorcererSubclassLevel[
            Literal[FirstSubclassPostLevel.SIXTH], Literal[SorcererSubclass.DIVINE_SOUL]
        ],
    ]
):
    """Increments sorcerer to level 6 and grants Divine Soul origin feature."""

    type: Literal[BuildingBlockType.SORCERER_LEVEL_6_DIVINE_SOUL] = (
        BuildingBlockType.SORCERER_LEVEL_6_DIVINE_SOUL
    )

    def _update_blueprint(self, blueprint: _BPT) -> _BPT:
        return blueprint.model_copy(
            update={
                "classes": blueprint.classes.model_copy(update={"sorcerer": 6}),
                "actions": blueprint.actions + (AbilityName.EMPOWERED_HEALING,),
            }
        )
