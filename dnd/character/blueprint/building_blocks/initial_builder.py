from __future__ import annotations

from typing import NamedTuple

from dnd.character.blueprint.building_blocks.all_choices_resolver import (
    AnyChoiceResolver,
)
from dnd.character.blueprint.building_blocks.building_block import (
    CombinedBlock,
)
from dnd.character.blueprint.building_blocks.level_assigner import (
    LevelAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner import (
    AnyRaceAssigner,
)
from dnd.character.blueprint.building_blocks.stats_builder import (
    AnyStatsBuilder,
)
from pydantic import Field


class InitialBuilderBlocks(NamedTuple):
    level_assigner: LevelAssigner
    stats_builder: AnyStatsBuilder
    race_assigner: AnyRaceAssigner
    all_choices_resolver: AnyChoiceResolver


class InitialBuilder(CombinedBlock):
    """Building block that performs initial character generation.

    Combines level assignment, ability score building, race selection,
    and choice resolution into a single orchestrated process.
    """

    blocks: InitialBuilderBlocks = Field(
        description="Building blocks for level, stats, race, and choices",
    )
