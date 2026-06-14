from typing import Annotated
from typing import Union

from dnd.character.blueprint.building_blocks.get_discriminator import (
    get_discriminator,
)
from dnd.character.blueprint.building_blocks.race_assigner.race_assigner import (
    RaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner.random_race_assigner import (
    RandomRaceAssigner,
)
from pydantic import Tag

AnyRaceAssigner = Annotated[
    Union[
        Annotated[RaceAssigner, Tag(RaceAssigner.get_block_type())],
        Annotated[RandomRaceAssigner, Tag(RandomRaceAssigner.get_block_type())],
    ],
    get_discriminator(),
]

__all__ = [
    "RaceAssigner",
    "RandomRaceAssigner",
    "AnyRaceAssigner",
]
