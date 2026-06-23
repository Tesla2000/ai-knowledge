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
from dnd.character.blueprint.building_blocks.subclass_assigner.subclass_assigner import (
    ArtificerSubclassAssigner,
)
from dnd.character.blueprint.building_blocks.subclass_assigner.subclass_assigner import (
    BarbarianSubclassAssigner,
)
from dnd.character.blueprint.building_blocks.subclass_assigner.subclass_assigner import (
    BardSubclassAssigner,
)
from dnd.character.blueprint.building_blocks.subclass_assigner.subclass_assigner import (
    ClericSubclassAssigner,
)
from dnd.character.blueprint.building_blocks.subclass_assigner.subclass_assigner import (
    DruidSubclassAssigner,
)
from dnd.character.blueprint.building_blocks.subclass_assigner.subclass_assigner import (
    FighterSubclassAssigner,
)
from dnd.character.blueprint.building_blocks.subclass_assigner.subclass_assigner import (
    MonkSubclassAssigner,
)
from dnd.character.blueprint.building_blocks.subclass_assigner.subclass_assigner import (
    PaladinSubclassAssigner,
)
from dnd.character.blueprint.building_blocks.subclass_assigner.subclass_assigner import (
    RangerSubclassAssigner,
)
from dnd.character.blueprint.building_blocks.subclass_assigner.subclass_assigner import (
    RogueSubclassAssigner,
)
from dnd.character.blueprint.building_blocks.subclass_assigner.subclass_assigner import (
    SorcererSubclassAssigner,
)
from dnd.character.blueprint.building_blocks.subclass_assigner.subclass_assigner import (
    WarlockSubclassAssigner,
)
from dnd.character.blueprint.building_blocks.subclass_assigner.subclass_assigner import (
    WizardSubclassAssigner,
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
        Annotated[
            ArtificerSubclassAssigner,
            Tag(ArtificerSubclassAssigner.get_block_type()),
        ],
        Annotated[
            BarbarianSubclassAssigner,
            Tag(BarbarianSubclassAssigner.get_block_type()),
        ],
        Annotated[BardSubclassAssigner, Tag(BardSubclassAssigner.get_block_type())],
        Annotated[ClericSubclassAssigner, Tag(ClericSubclassAssigner.get_block_type())],
        Annotated[DruidSubclassAssigner, Tag(DruidSubclassAssigner.get_block_type())],
        Annotated[
            FighterSubclassAssigner, Tag(FighterSubclassAssigner.get_block_type())
        ],
        Annotated[MonkSubclassAssigner, Tag(MonkSubclassAssigner.get_block_type())],
        Annotated[
            PaladinSubclassAssigner, Tag(PaladinSubclassAssigner.get_block_type())
        ],
        Annotated[RangerSubclassAssigner, Tag(RangerSubclassAssigner.get_block_type())],
        Annotated[RogueSubclassAssigner, Tag(RogueSubclassAssigner.get_block_type())],
        Annotated[
            SorcererSubclassAssigner, Tag(SorcererSubclassAssigner.get_block_type())
        ],
        Annotated[
            WarlockSubclassAssigner, Tag(WarlockSubclassAssigner.get_block_type())
        ],
        Annotated[WizardSubclassAssigner, Tag(WizardSubclassAssigner.get_block_type())],
    ],
    get_discriminator(),
]

__all__ = [
    "AISubclassAssigner",
    "ArtificerSubclassAssigner",
    "BarbarianSubclassAssigner",
    "BardSubclassAssigner",
    "ClericSubclassAssigner",
    "DruidSubclassAssigner",
    "FighterSubclassAssigner",
    "MonkSubclassAssigner",
    "OptionalSubclassAssigner",
    "PaladinSubclassAssigner",
    "RangerSubclassAssigner",
    "RandomSubclassAssigner",
    "RogueSubclassAssigner",
    "SorcererSubclassAssigner",
    "WarlockSubclassAssigner",
    "WizardSubclassAssigner",
]
