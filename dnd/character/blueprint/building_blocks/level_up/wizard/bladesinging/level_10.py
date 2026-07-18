from typing import Literal

from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.base import (
    WizardSubclassFeatureLevelBase,
)
from dnd.character.blueprint.sentinels import SecondSubclassPostLevel
from dnd.character.blueprint.sentinels import WizardSubclassLevel
from dnd.character.blueprint.states.state import _BPT
from dnd.choices.class_creation.character_class import WizardSubclass

from dnd.character._ability_name import AbilityName


class WizardLevel10Bladesinging(
    WizardSubclassFeatureLevelBase[
        WizardSubclassLevel[
            Literal[SecondSubclassPostLevel.NINTH], Literal[WizardSubclass.BLADESINGING]
        ],
        WizardSubclassLevel[
            Literal[SecondSubclassPostLevel.TENTH], Literal[WizardSubclass.BLADESINGING]
        ],
    ]
):
    """Increments wizard to level 10 and grants Bladesinging subclass feature."""

    type: Literal[BuildingBlockType.WIZARD_LEVEL_10_BLADESINGING] = (
        BuildingBlockType.WIZARD_LEVEL_10_BLADESINGING
    )

    def _update_blueprint(self, blueprint: _BPT) -> _BPT:
        return blueprint.model_copy(
            update={
                "classes": blueprint.classes.model_copy(update={"wizard": 10}),
                "actions": blueprint.actions + (AbilityName.SONG_OF_DEFENSE,),
            }
        )
