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


class WizardLevel6Conjuration(
    WizardSubclassFeatureLevelBase[
        WizardSubclassLevel[
            Literal[SecondSubclassPostLevel.FIFTH], Literal[WizardSubclass.CONJURATION]
        ],
        WizardSubclassLevel[
            Literal[SecondSubclassPostLevel.SIXTH], Literal[WizardSubclass.CONJURATION]
        ],
    ]
):
    """Increments wizard to level 6 and grants Conjuration subclass feature."""

    type: Literal[BuildingBlockType.WIZARD_LEVEL_6_CONJURATION] = (
        BuildingBlockType.WIZARD_LEVEL_6_CONJURATION
    )

    def _update_blueprint(self, blueprint: _BPT) -> _BPT:
        return blueprint.model_copy(
            update={
                "classes": blueprint.classes.model_copy(update={"wizard": 6}),
                "actions": blueprint.actions + (AbilityName.BENIGN_TRANSPOSITION,),
            }
        )
