"""All choices resolver package.

Provides two implementations:
- AllChoicesResolver: Chains individual resolvers (composable)
- AIAllChoicesResolver: Makes all choices in single LLM call (holistic)
"""

from __future__ import annotations

from typing import Annotated
from typing import Union

from dnd.character.blueprint.building_blocks.all_choices_resolver.ai import (
    AIAllChoicesResolver,
)
from dnd.character.blueprint.building_blocks.all_choices_resolver.base import (
    AllChoicesResolver,
)
from dnd.character.blueprint.building_blocks.all_choices_resolver.choice_package import (
    ChoicePackage,
)
from pydantic import Field

AnyChoiceResolver = Annotated[
    Union[
        AllChoicesResolver,
        AIAllChoicesResolver,
    ],
    Field(discriminator="type"),
]

__all__ = [
    "AllChoicesResolver",
    "AIAllChoicesResolver",
    "ChoicePackage",
]
