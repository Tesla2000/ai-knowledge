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
from pydantic import Field

AnyFeatChoiceResolver = Annotated[
    Union[
        RandomFeatChoiceResolver,
        AIFeatChoiceResolver,
        MaxFirstResolver,
        MaxIfNotMaxedResolver,
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
