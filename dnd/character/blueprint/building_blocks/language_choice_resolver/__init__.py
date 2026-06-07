from __future__ import annotations

from typing import Annotated
from typing import Union

from dnd.character.blueprint.building_blocks.get_discriminator import (
    get_discriminator,
)
from dnd.character.blueprint.building_blocks.language_choice_resolver.ai import (
    AILanguageChoiceResolver,
)
from dnd.character.blueprint.building_blocks.language_choice_resolver.random import (
    RandomLanguageChoiceResolver,
)
from pydantic import Tag

AnyLanguageChoiceResolver = Annotated[
    Union[
        Annotated[
            RandomLanguageChoiceResolver,
            Tag(RandomLanguageChoiceResolver.get_block_type()),
        ],
        Annotated[
            AILanguageChoiceResolver,
            Tag(AILanguageChoiceResolver.get_block_type()),
        ],
    ],
    get_discriminator(),
]

__all__ = [
    "RandomLanguageChoiceResolver",
    "AILanguageChoiceResolver",
    "AnyLanguageChoiceResolver",
]
