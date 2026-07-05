from __future__ import annotations

from typing import Annotated
from typing import Union

from dnd.character.blueprint.building_blocks.feat_choice_resolver.ai import (
    AIFeatChoiceResolver,
)
from dnd.character.blueprint.building_blocks.feat_choice_resolver.max_first import (
    MaxFirstResolver,
)
from dnd.character.blueprint.building_blocks.feat_choice_resolver.max_if_not_maxed import (
    MaxIfNotMaxedResolver,
)
from dnd.character.blueprint.building_blocks.feat_choice_resolver.random import (
    RandomFeatChoiceResolver,
)
from dnd.character.blueprint.state import HasClasses
from dnd.character.blueprint.state import HasFeats
from dnd.character.blueprint.state import HasStats
from dnd.character.blueprint.state import HasStatsCup
from pydantic import Field
from typing_protocol_intersection import ProtocolIntersection

AnyFeatChoiceResolver = Annotated[
    Union[
        RandomFeatChoiceResolver[
            ProtocolIntersection[ProtocolIntersection[HasFeats, HasStats], HasClasses]
        ],
        AIFeatChoiceResolver[
            ProtocolIntersection[ProtocolIntersection[HasFeats, HasStats], HasClasses]
        ],
        MaxFirstResolver[
            ProtocolIntersection[
                ProtocolIntersection[
                    ProtocolIntersection[HasFeats, HasStats], HasClasses
                ],
                HasStatsCup,
            ]
        ],
        MaxIfNotMaxedResolver[
            ProtocolIntersection[
                ProtocolIntersection[
                    ProtocolIntersection[HasFeats, HasStats], HasClasses
                ],
                HasStatsCup,
            ]
        ],
    ],
    Field(discriminator="type"),
]

__all__ = [
    "RandomFeatChoiceResolver",
    "AIFeatChoiceResolver",
    "MaxFirstResolver",
    "MaxIfNotMaxedResolver",
    "AnyFeatChoiceResolver",
]
