from typing import Literal

from pydantic import Field

from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)
from dnd.character.blueprint.building_blocks.level_up.barbarian.base import (
    BarbarianSubclassFeatureLevelBase,
)
from dnd.character.blueprint.building_blocks.totem_choice_resolver import (
    AnyTotemChoiceResolver,
)
from dnd.character.blueprint.building_blocks.totem_choice_resolver.random import (
    RandomTotemChoiceResolver,
)
from dnd.character.blueprint.sentinels import ClassSubclassLevel
from dnd.character.blueprint.sentinels import ThirdSubclassPostLevel
from dnd.choices.class_creation.character_class import BarbarianSubclass
from dnd.character.blueprint.states.state import _BPT
from dnd.character._ability_name import AbilityName


class BarbarianLevel14TotemWarrior(
    BarbarianSubclassFeatureLevelBase[
        ClassSubclassLevel[
            Literal[ThirdSubclassPostLevel.THIRTEENTH], BarbarianSubclass
        ],
        ClassSubclassLevel[
            Literal[ThirdSubclassPostLevel.FOURTEENTH], BarbarianSubclass
        ],
    ]
):
    """Grants Totem Warrior level 14 subclass feature."""

    type: Literal[BuildingBlockType.BARBARIAN_LEVEL_14_TOTEM_WARRIOR] = (
        BuildingBlockType.BARBARIAN_LEVEL_14_TOTEM_WARRIOR
    )
    attunement_resolver: AnyTotemChoiceResolver = Field(
        default_factory=RandomTotemChoiceResolver
    )

    def _update_blueprint(self, blueprint: _BPT) -> _BPT:
        return blueprint.model_copy(
            update={
                "classes": blueprint.classes.model_copy(update={"barbarian": 14}),
                "actions": blueprint.actions + (AbilityName.TOTEMIC_ATTUNEMENT,),
            }
        )
