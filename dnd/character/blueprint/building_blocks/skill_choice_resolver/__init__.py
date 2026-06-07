from __future__ import annotations

from typing import Annotated
from typing import Union

from dnd.character.blueprint.building_blocks.get_discriminator import (
    get_discriminator,
)
from dnd.character.blueprint.building_blocks.skill_choice_resolver.ai import (
    AISkillChoiceResolver,
)
from dnd.character.blueprint.building_blocks.skill_choice_resolver.random import (
    RandomSkillChoiceResolver,
)
from pydantic import Tag

AnySkillChoiceResolver = Annotated[
    Union[
        Annotated[
            RandomSkillChoiceResolver,
            Tag(RandomSkillChoiceResolver.get_block_type()),
        ],
        Annotated[
            AISkillChoiceResolver,
            Tag(AISkillChoiceResolver.get_block_type()),
        ],
    ],
    get_discriminator(),
]

__all__ = [
    "AISkillChoiceResolver",
    "RandomSkillChoiceResolver",
    "AnySkillChoiceResolver",
]
