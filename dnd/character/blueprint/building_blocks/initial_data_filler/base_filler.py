from __future__ import annotations

from abc import ABC

from dnd.character.blueprint.building_blocks.building_block import BuildingBlock
from dnd.character.blueprint.state import BlueprintProtocol
from dnd.character.blueprint.state import HasInitialData
from dnd.character.delta.initial_data_delta import InitialDataDelta
from pydantic import ConfigDict


class InitialDataFiller(
    BuildingBlock[BlueprintProtocol, InitialDataDelta, HasInitialData], ABC
):
    model_config = ConfigDict(frozen=True)
