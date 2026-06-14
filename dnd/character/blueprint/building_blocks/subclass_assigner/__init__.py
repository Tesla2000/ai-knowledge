"""Subclass assignment building blocks.

This package provides building blocks for assigning subclasses to characters,
including both random and AI-powered selection strategies.
"""

from __future__ import annotations

from typing import Annotated
from typing import Union

from dnd.character.blueprint.building_blocks.get_discriminator import (
    get_discriminator,
)
from dnd.character.blueprint.building_blocks.subclass_assigner.ai import (
    AISubclassAssigner,
)
from dnd.character.blueprint.building_blocks.subclass_assigner.optional import (
    OptionalSubclassAssigner,
)
from dnd.character.blueprint.building_blocks.subclass_assigner.random import (
    RandomSubclassAssigner,
)
from pydantic import Tag

AnySubclassAssigner = Annotated[
    Union[
        Annotated[
            RandomSubclassAssigner,
            Tag(RandomSubclassAssigner.get_block_type()),
        ],
        Annotated[
            OptionalSubclassAssigner,
            Tag(OptionalSubclassAssigner.get_block_type()),
        ],
        Annotated[AISubclassAssigner, Tag(AISubclassAssigner.get_block_type())],
    ],
    get_discriminator(),
]

__all__ = [
    "AISubclassAssigner",
    "OptionalSubclassAssigner",
    "RandomSubclassAssigner",
]
