from __future__ import annotations

from typing import Annotated
from typing import Union

from dnd.character.blueprint.building_blocks.level_up.spell_assignment.llm import (
    SorcererLLMSpellAssigner,
    WizardLLMSpellAssigner,
)
from dnd.character.blueprint.building_blocks.level_up.spell_assignment.random import (
    SorcererRandomSpellAssigner,
    WizardRandomSpellAssigner,
)
from dnd.character.blueprint.state import HasSorcererLevel
from dnd.character.blueprint.state import HasWizardLevel
from pydantic import Field

AnySpellAssigner = Annotated[
    Union[
        WizardRandomSpellAssigner[HasWizardLevel],
        SorcererRandomSpellAssigner[HasSorcererLevel],
        WizardLLMSpellAssigner[HasWizardLevel],
        SorcererLLMSpellAssigner[HasSorcererLevel],
    ],
    Field(discriminator="type"),
]

__all__ = [
    "WizardRandomSpellAssigner",
    "SorcererRandomSpellAssigner",
    "WizardLLMSpellAssigner",
    "SorcererLLMSpellAssigner",
    "AnySpellAssigner",
]
