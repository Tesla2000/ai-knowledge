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


class SorcererLevel18DraconicBloodline(
    SorcererSubclassFeatureLevelBase[
        SorcererSubclassLevel[
            Literal[FirstSubclassPostLevel.SEVENTEENTH],
            Literal[SorcererSubclass.DRACONIC_BLOODLINE],
        ],
        SorcererSubclassLevel[
            Literal[FirstSubclassPostLevel.EIGHTEENTH],
            Literal[SorcererSubclass.DRACONIC_BLOODLINE],
        ],
    ]
):
    """Increments sorcerer to level 18 and grants Draconic Bloodline origin feature."""

    type: Literal[BuildingBlockType.SORCERER_LEVEL_18_DRACONIC_BLOODLINE] = (
        BuildingBlockType.SORCERER_LEVEL_18_DRACONIC_BLOODLINE
    )

    def _update_blueprint(self, blueprint: _BPT) -> _BPT:
        return blueprint.model_copy(
            update={
                "classes": blueprint.classes.model_copy(update={"sorcerer": 18}),
                "actions": blueprint.actions + (AbilityName.DRACONIC_PRESENCE,),
            }
        )
