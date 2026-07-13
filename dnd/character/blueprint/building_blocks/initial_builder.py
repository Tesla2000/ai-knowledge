from typing import Literal
from typing import TypeAlias

from dnd.character.blueprint.building_blocks.all_choices_resolver import (
    AnyChoiceResolver,
)
from dnd.character.blueprint.building_blocks.building_block import BuildingBlock
from dnd.character.blueprint.building_blocks.level_assigner import LevelAssigner
from dnd.character.blueprint.building_blocks.race_assigner import AnyRaceAssigner
from dnd.character.blueprint.building_blocks.stats_builder import AnyStatsBuilder
from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)
from dnd.character.blueprint.sentinels import (
    ClassPreSubclassLevel,
    SorcererPreSubclassLevel,
    ThirdSubclassPreLevel,
    FirstSubclassPreLevel,
    SecondSubclassPreLevel,
    WizardPreSubclassLevel,
)
from dnd.character.blueprint.states.state import Blueprint
from dnd.character.blueprint.states.state import EmptyBlueprint
from dnd.character.race.race import Race
from dnd.character.stats import Stats

_Z = Literal[SecondSubclassPreLevel.ZEROTH]
_SZ = Literal[FirstSubclassPreLevel.ZEROTH]
_TZ = Literal[ThirdSubclassPreLevel.ZEROTH]

InitializedBlueprint: TypeAlias = Blueprint[
    Race,
    Stats,
    None,
    Literal[0],
    Literal[0],
    WizardPreSubclassLevel[_Z, None],
    SorcererPreSubclassLevel[_SZ, None],
    ClassPreSubclassLevel[_TZ, None],
    ClassPreSubclassLevel[_TZ, None],
    ClassPreSubclassLevel[_TZ, None],
    ClassPreSubclassLevel[_TZ, None],
    ClassPreSubclassLevel[_TZ, None],
    ClassPreSubclassLevel[_TZ, None],
    ClassPreSubclassLevel[_TZ, None],
    ClassPreSubclassLevel[_TZ, None],
    ClassPreSubclassLevel[_TZ, None],
    ClassPreSubclassLevel[_TZ, None],
    ClassPreSubclassLevel[_TZ, None],
    None,
]


class InitialBuilder(BuildingBlock):
    """Combines level assignment, stats, race, and choice resolution."""

    type: Literal[BuildingBlockType.INITIAL_BUILDER] = BuildingBlockType.INITIAL_BUILDER

    level_assigner: LevelAssigner
    stats_builder: AnyStatsBuilder
    race_assigner: AnyRaceAssigner
    all_choices_resolver: AnyChoiceResolver

    def apply(self, blueprint: EmptyBlueprint) -> InitializedBlueprint:
        r1 = self.level_assigner.apply(blueprint)
        r2 = self.stats_builder.apply(r1)
        r3 = self.race_assigner.apply(r2)
        return self.all_choices_resolver.apply(r3)
