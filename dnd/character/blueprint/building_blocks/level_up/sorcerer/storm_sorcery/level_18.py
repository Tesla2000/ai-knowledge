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


class SorcererLevel18StormSorcery(
    SorcererSubclassFeatureLevelBase[
        SorcererSubclassLevel[
            Literal[FirstSubclassPostLevel.SEVENTEENTH],
            Literal[SorcererSubclass.STORM_SORCERY],
        ],
        SorcererSubclassLevel[
            Literal[FirstSubclassPostLevel.EIGHTEENTH],
            Literal[SorcererSubclass.STORM_SORCERY],
        ],
    ]
):
    """Increments sorcerer to level 18 and grants Storm Sorcery origin feature."""

    type: Literal[BuildingBlockType.SORCERER_LEVEL_18_STORM_SORCERY] = (
        BuildingBlockType.SORCERER_LEVEL_18_STORM_SORCERY
    )

    def _update_blueprint(self, blueprint: _BPT) -> _BPT:
        return blueprint.model_copy(
            update={
                "classes": blueprint.classes.model_copy(update={"sorcerer": 18}),
                "actions": blueprint.actions + (AbilityName.WIND_SOUL,),
            }
        )
