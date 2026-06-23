from __future__ import annotations

from typing import Annotated
from typing import Union

from dnd.character.blueprint.building_blocks.get_discriminator import (
    get_discriminator,
)
from dnd.character.blueprint.building_blocks.level_up.spell_assignment.llm import (
    SorcererLLMSpellAssigner,
    WizardLLMSpellAssigner,
)
from dnd.character.blueprint.building_blocks.level_up.spell_assignment.random import (
    SorcererRandomSpellAssigner,
    WizardRandomSpellAssigner,
)
from pydantic import Tag

AnySpellAssigner = Annotated[
    Union[
        Annotated[
            WizardRandomSpellAssigner,
            Tag(WizardRandomSpellAssigner.get_block_type()),
        ],
        Annotated[
            SorcererRandomSpellAssigner,
            Tag(SorcererRandomSpellAssigner.get_block_type()),
        ],
        Annotated[
            WizardLLMSpellAssigner,
            Tag(WizardLLMSpellAssigner.get_block_type()),
        ],
        Annotated[
            SorcererLLMSpellAssigner,
            Tag(SorcererLLMSpellAssigner.get_block_type()),
        ],
    ],
    get_discriminator(),
]

__all__ = [
    "WizardRandomSpellAssigner",
    "SorcererRandomSpellAssigner",
    "WizardLLMSpellAssigner",
    "SorcererLLMSpellAssigner",
    "AnySpellAssigner",
]
