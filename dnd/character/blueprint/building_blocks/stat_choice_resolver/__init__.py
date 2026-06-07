from __future__ import annotations

from typing import Annotated
from typing import Union

from dnd.character.blueprint.building_blocks.get_discriminator import (
    get_discriminator,
)
from dnd.character.blueprint.building_blocks.stat_choice_resolver.ai import (
    AIStatChoiceResolver,
)
from dnd.character.blueprint.building_blocks.stat_choice_resolver.priority import (
    PriorityStatChoiceResolver,
)
from pydantic import Tag

AnyStatChoiceResolver = Annotated[
    Union[
        Annotated[
            PriorityStatChoiceResolver,
            Tag(PriorityStatChoiceResolver.get_block_type()),
        ],
        Annotated[
            AIStatChoiceResolver, Tag(AIStatChoiceResolver.get_block_type())
        ],
    ],
    get_discriminator(),
]

__all__ = [
    "AIStatChoiceResolver",
    "PriorityStatChoiceResolver",
    "AnyStatChoiceResolver",
]
