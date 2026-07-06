from __future__ import annotations

from typing import Annotated
from typing import Union

from dnd.character.blueprint.building_blocks.skill_choice_resolver.ai import (
    AISkillChoiceResolver,
)
from dnd.character.blueprint.building_blocks.skill_choice_resolver.random import (
    RandomSkillChoiceResolver,
)
from pydantic import Field

AnySkillChoiceResolver = Annotated[
    Union[
        RandomSkillChoiceResolver,
        AISkillChoiceResolver,
    ],
    Field(discriminator="type"),
]

__all__ = [
    "AISkillChoiceResolver",
    "RandomSkillChoiceResolver",
    "AnySkillChoiceResolver",
]
