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
from dnd.character.blueprint.building_blocks.get_discriminator import (
    get_discriminator,
)
from pydantic import Tag

AnyFeatChoiceResolver = Annotated[
    Union[
        Annotated[
            RandomFeatChoiceResolver,
            Tag(RandomFeatChoiceResolver.get_block_type()),
        ],
        Annotated[
            AIFeatChoiceResolver, Tag(AIFeatChoiceResolver.get_block_type())
        ],
        Annotated[MaxFirstResolver, Tag(MaxFirstResolver.get_block_type())],
        Annotated[
            MaxIfNotMaxedResolver, Tag(MaxIfNotMaxedResolver.get_block_type())
        ],
    ],
    get_discriminator(),
]

__all__ = [
    "RandomFeatChoiceResolver",
    "AIFeatChoiceResolver",
    "MaxFirstResolver",
    "MaxIfNotMaxedResolver",
    "AnyFeatChoiceResolver",
]
