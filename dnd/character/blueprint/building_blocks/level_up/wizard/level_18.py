from typing import Literal

from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.base import (
    WizardLevel18UpgradeLevelBase,
)
from dnd.character.blueprint.sentinels import SecondSubclassPostLevel
from dnd.character.blueprint.states.state import _BPT

from dnd.character._ability_name import AbilityName


class WizardLevel18(
    WizardLevel18UpgradeLevelBase[
        Literal[SecondSubclassPostLevel.SEVENTEENTH],
        Literal[SecondSubclassPostLevel.EIGHTEENTH],
    ]
):
    """Increments wizard to level 18 and transitions to WizardLevel18Blueprint."""

    type: Literal[BuildingBlockType.WIZARD_LEVEL_18] = BuildingBlockType.WIZARD_LEVEL_18

    def _update_blueprint(self, blueprint: _BPT) -> _BPT:
        return blueprint.model_copy(
            update={
                "classes": blueprint.classes.model_copy(update={"wizard": 18}),
                "actions": blueprint.actions + (AbilityName.SPELL_MASTERY,),
            }
        )
