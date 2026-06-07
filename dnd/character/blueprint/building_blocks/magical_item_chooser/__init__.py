"""Magical item chooser package.

Provides implementations for selecting magical items:
- RandomMagicalItemChooser: Random level-by-level selection with optional seed
- AIMagicalItemChooser: Holistic AI-powered selection
- MagicalItemChooserBase: Abstract base for all choosers
"""

from __future__ import annotations

from typing import Annotated
from typing import Union

from dnd.character.blueprint.building_blocks.get_discriminator import (
    get_discriminator,
)
from dnd.character.blueprint.building_blocks.magical_item_chooser.ai import (
    AIMagicalItemChooser,
)
from dnd.character.blueprint.building_blocks.magical_item_chooser.random import (
    RandomMagicalItemChooser,
)
from pydantic import Tag

AnyMagicalItemChooser = Annotated[
    Union[
        Annotated[
            RandomMagicalItemChooser,
            Tag(RandomMagicalItemChooser.get_block_type()),
        ],
        Annotated[
            AIMagicalItemChooser,
            Tag(AIMagicalItemChooser.get_block_type()),
        ],
    ],
    get_discriminator(),
]

__all__ = [
    "RandomMagicalItemChooser",
    "AIMagicalItemChooser",
    "AnyMagicalItemChooser",
]
