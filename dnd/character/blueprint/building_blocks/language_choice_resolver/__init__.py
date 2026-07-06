from __future__ import annotations

from typing import Annotated
from typing import Union

from dnd.character.blueprint.building_blocks.language_choice_resolver.ai import (
    AILanguageChoiceResolver,
)
from dnd.character.blueprint.building_blocks.language_choice_resolver.random import (
    RandomLanguageChoiceResolver,
)
from pydantic import Field

AnyLanguageChoiceResolver = Annotated[
    Union[
        RandomLanguageChoiceResolver,
        AILanguageChoiceResolver,
    ],
    Field(discriminator="type"),
]

__all__ = [
    "RandomLanguageChoiceResolver",
    "AILanguageChoiceResolver",
    "AnyLanguageChoiceResolver",
]
