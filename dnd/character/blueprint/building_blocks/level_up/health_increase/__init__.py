from __future__ import annotations

from typing import Annotated
from typing import Union

from dnd.character.blueprint.building_blocks.get_discriminator import (
    get_discriminator,
)
from dnd.character.blueprint.building_blocks.level_up.health_increase.average import (
    HealthIncreaseAverage,
)
from dnd.character.blueprint.building_blocks.level_up.health_increase.random import (
    HealthIncreaseRandom,
)
from dnd.character.blueprint.building_blocks.level_up.health_increase.random_min_two import (
    HealthIncreaseRandomMinTwo,
)
from dnd.character.blueprint.building_blocks.level_up.health_increase.random_reroll_ones import (
    HealthIncreaseRandomRerollOnes,
)
from pydantic import Tag

AnyHealthIncrease = Annotated[
    Union[
        Annotated[
            HealthIncreaseAverage,
            Tag(HealthIncreaseAverage.get_block_type()),
        ],
        Annotated[
            HealthIncreaseRandom,
            Tag(HealthIncreaseRandom.get_block_type()),
        ],
        Annotated[
            HealthIncreaseRandomMinTwo,
            Tag(HealthIncreaseRandomMinTwo.get_block_type()),
        ],
        Annotated[
            HealthIncreaseRandomRerollOnes,
            Tag(HealthIncreaseRandomRerollOnes.get_block_type()),
        ],
    ],
    get_discriminator(),
]

__all__ = [
    "HealthIncreaseAverage",
    "HealthIncreaseRandom",
    "HealthIncreaseRandomMinTwo",
    "HealthIncreaseRandomRerollOnes",
    "AnyHealthIncrease",
]
