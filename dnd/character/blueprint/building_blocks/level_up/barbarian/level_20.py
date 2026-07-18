from typing import Literal

from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)
from dnd.character.blueprint.building_blocks.level_up.barbarian.base import (
    BarbarianSharedLevelBase,
)
from dnd.character.blueprint.sentinels import ThirdSubclassPostLevel
from dnd.character.blueprint.states.state import _BPT
from dnd.character.stats import Stats

from dnd.character._ability_name import AbilityName


class BarbarianLevel20(
    BarbarianSharedLevelBase[
        Literal[ThirdSubclassPostLevel.NINETEENTH],
        Literal[ThirdSubclassPostLevel.TWENTIETH],
    ]
):
    """Increments barbarian to level 20."""

    type: Literal[BuildingBlockType.BARBARIAN_LEVEL_20] = (
        BuildingBlockType.BARBARIAN_LEVEL_20
    )

    def _update_blueprint(self, blueprint: _BPT) -> _BPT:
        old_cup = blueprint.stats_cup
        new_cup = Stats(
            strength=max(old_cup.strength, 24),
            dexterity=old_cup.dexterity,
            constitution=max(old_cup.constitution, 24),
            intelligence=old_cup.intelligence,
            wisdom=old_cup.wisdom,
            charisma=old_cup.charisma,
        )
        return blueprint.model_copy(
            update={
                "classes": blueprint.classes.model_copy(update={"barbarian": 20}),
                "stats_cup": new_cup,
                "actions": blueprint.actions + (AbilityName.PRIMAL_CHAMPION,),
            }
        )
