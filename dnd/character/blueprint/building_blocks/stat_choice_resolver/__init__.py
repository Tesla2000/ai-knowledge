from __future__ import annotations

from typing import Annotated
from typing import Union

from dnd.character.blueprint.building_blocks.stat_choice_resolver.ai import (
    AIStatChoiceResolver,
)
from dnd.character.blueprint.building_blocks.stat_choice_resolver.priority import (
    PriorityStatChoiceResolver,
)
from pydantic import Field

AnyStatChoiceResolver = Annotated[
    Union[
        PriorityStatChoiceResolver,
        AIStatChoiceResolver,
    ],
    Field(discriminator="type"),
]

__all__ = [
    "AIStatChoiceResolver",
    "PriorityStatChoiceResolver",
    "AnyStatChoiceResolver",
]
