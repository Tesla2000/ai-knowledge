from typing import Annotated
from typing import Union

from dnd.character.blueprint.building_blocks.tool_proficiency_choice_resolver.ai import (
    AIToolProficiencyChoiceResolver,
)
from dnd.character.blueprint.building_blocks.tool_proficiency_choice_resolver.random import (
    RandomToolProficiencyChoiceResolver,
)
from pydantic import Field

AnyToolProficiencyChoiceResolver = Annotated[
    Union[
        RandomToolProficiencyChoiceResolver,
        AIToolProficiencyChoiceResolver,
    ],
    Field(discriminator="type"),
]

__all__ = [
    "RandomToolProficiencyChoiceResolver",
    "AIToolProficiencyChoiceResolver",
    "AnyToolProficiencyChoiceResolver",
]
