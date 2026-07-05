from __future__ import annotations

from typing import Annotated
from typing import Union

from dnd.character.blueprint.building_blocks.stat_choice_resolver.ai import (
    AIStatChoiceResolver,
)
from dnd.character.blueprint.building_blocks.stat_choice_resolver.priority import (
    PriorityStatChoiceResolver,
)
from dnd.character.blueprint.state import HasNStatChoices
from dnd.character.blueprint.state import HasStats
from pydantic import Field
from typing_protocol_intersection import ProtocolIntersection

AnyStatChoiceResolver = Annotated[
    Union[
        PriorityStatChoiceResolver[ProtocolIntersection[HasStats, HasNStatChoices]],
        AIStatChoiceResolver[ProtocolIntersection[HasStats, HasNStatChoices]],
    ],
    Field(discriminator="type"),
]

__all__ = [
    "AIStatChoiceResolver",
    "PriorityStatChoiceResolver",
    "AnyStatChoiceResolver",
]
