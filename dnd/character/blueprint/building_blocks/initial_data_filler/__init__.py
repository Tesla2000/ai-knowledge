from typing import Annotated
from typing import Union

from dnd.character.blueprint.building_blocks.initial_data_filler.ai_base_builder_assigner import (
    AIBaseBuilderAssigner,
)
from dnd.character.blueprint.building_blocks.initial_data_filler.ai_partial_builder_assigner import (
    AIPartialBuilderAssigner,
)
from dnd.character.blueprint.building_blocks.initial_data_filler.random_filler import (
    RandomInitialDataFiller,
)
from pydantic import Field

AnyInitialDataFiller = Annotated[
    Union[
        RandomInitialDataFiller,
        AIBaseBuilderAssigner,
        AIPartialBuilderAssigner,
    ],
    Field(discriminator="type"),
]

__all__ = [
    "AIBaseBuilderAssigner",
    "AIPartialBuilderAssigner",
    "RandomInitialDataFiller",
    "AnyInitialDataFiller",
]
