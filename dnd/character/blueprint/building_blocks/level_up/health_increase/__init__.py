from __future__ import annotations

from typing import Annotated
from typing import Union

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
from pydantic import Field

AnyHealthIncrease = Annotated[
    Union[
        HealthIncreaseAverage,
        HealthIncreaseRandom,
        HealthIncreaseRandomMinTwo,
        HealthIncreaseRandomRerollOnes,
    ],
    Field(discriminator="type"),
]

__all__ = [
    "HealthIncreaseAverage",
    "HealthIncreaseRandom",
    "HealthIncreaseRandomMinTwo",
    "HealthIncreaseRandomRerollOnes",
    "AnyHealthIncrease",
]
