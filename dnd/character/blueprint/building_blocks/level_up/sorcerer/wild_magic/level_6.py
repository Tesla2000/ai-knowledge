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


class SorcererLevel6WildMagic(
    SorcererSubclassFeatureLevelBase[
        SorcererSubclassLevel[
            Literal[FirstSubclassPostLevel.FIFTH], Literal[SorcererSubclass.WILD_MAGIC]
        ],
        SorcererSubclassLevel[
            Literal[FirstSubclassPostLevel.SIXTH], Literal[SorcererSubclass.WILD_MAGIC]
        ],
    ]
):
    """Increments sorcerer to level 6 and grants Wild Magic origin feature."""

    type: Literal[BuildingBlockType.SORCERER_LEVEL_6_WILD_MAGIC] = (
        BuildingBlockType.SORCERER_LEVEL_6_WILD_MAGIC
    )

    def _update_blueprint(self, blueprint: _BPT) -> _BPT:
        return blueprint.model_copy(
            update={
                "classes": blueprint.classes.model_copy(update={"sorcerer": 6}),
                "actions": blueprint.actions + (AbilityName.BEND_LUCK,),
            }
        )
