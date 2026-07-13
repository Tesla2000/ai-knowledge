from typing import Annotated
from typing import Union

from pydantic import Field

from dnd.character.blueprint.building_blocks.metamagic_choice_resolver.base import (
    MetamagicChoiceResolver,
)
from dnd.character.blueprint.building_blocks.metamagic_choice_resolver.random import (
    RandomMetamagicChoiceResolver,
)

AnyMetamagicChoiceResolver = Annotated[
    Union[RandomMetamagicChoiceResolver,],
    Field(discriminator="type"),
]

__all__ = [
    "MetamagicChoiceResolver",
    "RandomMetamagicChoiceResolver",
    "AnyMetamagicChoiceResolver",
]
