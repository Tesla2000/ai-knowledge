"""Subclass assignment building blocks.

This package provides building blocks for assigning subclasses to characters,
including both random and AI-powered selection strategies.
"""

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
