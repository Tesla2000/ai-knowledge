from typing import Literal

from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.base import (
    WizardPreSubclassLevelBase,
)
from dnd.character.blueprint.sentinels import SecondSubclassPostLevel
from dnd.character.blueprint.sentinels import SecondSubclassPreLevel
from dnd.character.blueprint.sentinels import WizardPreSubclassLevel
from dnd.character.blueprint.sentinels import WizardSubclassLevel
from dnd.character.blueprint.states.state import _BPT
from dnd.choices.class_creation.character_class import WizardSubclass

from dnd.character._ability_name import AbilityName


class WizardLevel2Chronurgy(
    WizardPreSubclassLevelBase[
        WizardPreSubclassLevel[Literal[SecondSubclassPreLevel.FIRST], None],
        WizardSubclassLevel[
            Literal[SecondSubclassPostLevel.SECOND], Literal[WizardSubclass.CHRONURGY]
        ],
    ]
):
    """Increments wizard to level 2 and assigns Chronurgy subclass."""

    type: Literal[BuildingBlockType.WIZARD_LEVEL_2_CHRONURGY] = (
        BuildingBlockType.WIZARD_LEVEL_2_CHRONURGY
    )

    def _update_blueprint(self, blueprint: _BPT) -> _BPT:
        return blueprint.model_copy(
            update={
                "classes": blueprint.classes.model_copy(update={"wizard": 2}),
                "subclasses": blueprint.subclasses + (WizardSubclass.CHRONURGY,),
                "actions": blueprint.actions
                + (AbilityName.CHRONAL_SHIFT, AbilityName.TEMPORAL_AWARENESS),
            }
        )
