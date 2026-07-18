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


class WizardLevel2Transmutation(
    WizardPreSubclassLevelBase[
        WizardPreSubclassLevel[Literal[SecondSubclassPreLevel.FIRST], None],
        WizardSubclassLevel[
            Literal[SecondSubclassPostLevel.SECOND],
            Literal[WizardSubclass.TRANSMUTATION],
        ],
    ]
):
    """Increments wizard to level 2 and assigns Transmutation subclass."""

    type: Literal[BuildingBlockType.WIZARD_LEVEL_2_TRANSMUTATION] = (
        BuildingBlockType.WIZARD_LEVEL_2_TRANSMUTATION
    )

    def _update_blueprint(self, blueprint: _BPT) -> _BPT:
        return blueprint.model_copy(
            update={
                "classes": blueprint.classes.model_copy(update={"wizard": 2}),
                "subclasses": blueprint.subclasses + (WizardSubclass.TRANSMUTATION,),
                "actions": blueprint.actions
                + (AbilityName.TRANSMUTATION_SAVANT, AbilityName.MINOR_ALCHEMY),
            }
        )
