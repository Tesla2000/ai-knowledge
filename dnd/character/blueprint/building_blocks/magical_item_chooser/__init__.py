"""Magical item chooser package.

Provides implementations for selecting magical items:
- RandomMagicalItemChooser: Random level-by-level selection with optional seed
- AIMagicalItemChooser: Holistic AI-powered selection
- MagicalItemChooserBase: Abstract base for all choosers
"""

from typing import Annotated
from typing import Union

from dnd.character.blueprint.building_blocks.magical_item_chooser.ai import (
    AIMagicalItemChooser,
)
from dnd.character.blueprint.building_blocks.magical_item_chooser.random import (
    RandomMagicalItemChooser,
)
from pydantic import Field

AnyMagicalItemChooser = Annotated[
    Union[
        RandomMagicalItemChooser,
        AIMagicalItemChooser,
    ],
    Field(discriminator="type"),
]

__all__ = [
    "RandomMagicalItemChooser",
    "AIMagicalItemChooser",
    "AnyMagicalItemChooser",
]
