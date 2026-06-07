from __future__ import annotations

from typing import Annotated
from typing import Union

from dnd.character.blueprint.building_blocks.get_discriminator import (
    get_discriminator,
)
from dnd.character.blueprint.building_blocks.initial_data_filler.ai_base_builder_assigner import (
    AIBaseBuilderAssigner,
)
from dnd.character.blueprint.building_blocks.initial_data_filler.ai_partial_builder_assigner import (
    AIPartialBuilderAssigner,
)
from dnd.character.blueprint.building_blocks.initial_data_filler.random_filler import (
    RandomInitialDataFiller,
)
from pydantic import Tag

AnyInitialDataFiller = Annotated[
    Union[
        Annotated[
            RandomInitialDataFiller,
            Tag(RandomInitialDataFiller.get_block_type()),
        ],
        Annotated[
            AIBaseBuilderAssigner,
            Tag(AIBaseBuilderAssigner.get_block_type()),
        ],
        Annotated[
            AIPartialBuilderAssigner,
            Tag(AIPartialBuilderAssigner.get_block_type()),
        ],
    ],
    get_discriminator(),
]

__all__ = [
    "AIBaseBuilderAssigner",
    "AIPartialBuilderAssigner",
    "RandomInitialDataFiller",
    "AnyInitialDataFiller",
]
