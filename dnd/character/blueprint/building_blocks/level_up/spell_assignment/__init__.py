from __future__ import annotations

from typing import Annotated
from typing import Union

from dnd.character.blueprint.building_blocks.get_discriminator import (
    get_discriminator,
)
from dnd.character.blueprint.building_blocks.level_up.spell_assignment.llm import (
    LLMSpellAssigner,
)
from dnd.character.blueprint.building_blocks.level_up.spell_assignment.random import (
    RandomSpellAssigner,
)
from pydantic import Tag

AnySpellAssigner = Annotated[
    Union[
        Annotated[
            RandomSpellAssigner,
            Tag(RandomSpellAssigner.get_block_type()),
        ],
        Annotated[LLMSpellAssigner, Tag(LLMSpellAssigner.get_block_type())],
    ],
    get_discriminator(),
]

__all__ = [
    "RandomSpellAssigner",
    "LLMSpellAssigner",
    "AnySpellAssigner",
]
