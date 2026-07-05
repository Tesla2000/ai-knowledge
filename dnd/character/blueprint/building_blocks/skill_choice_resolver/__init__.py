from __future__ import annotations

from typing import Annotated
from typing import Union

from dnd.character.blueprint.building_blocks.skill_choice_resolver.ai import (
    AISkillChoiceResolver,
)
from dnd.character.blueprint.building_blocks.skill_choice_resolver.random import (
    RandomSkillChoiceResolver,
)
from dnd.character.blueprint.state import HasNSkillChoices
from dnd.character.blueprint.state import HasSkillProficiencies
from dnd.character.blueprint.state import HasSkillsToChooseFrom
from pydantic import Field
from typing_protocol_intersection import ProtocolIntersection

AnySkillChoiceResolver = Annotated[
    Union[
        RandomSkillChoiceResolver[
            ProtocolIntersection[
                ProtocolIntersection[HasNSkillChoices, HasSkillsToChooseFrom],
                HasSkillProficiencies,
            ]
        ],
        AISkillChoiceResolver[
            ProtocolIntersection[
                ProtocolIntersection[HasNSkillChoices, HasSkillsToChooseFrom],
                HasSkillProficiencies,
            ]
        ],
    ],
    Field(discriminator="type"),
]

__all__ = [
    "AISkillChoiceResolver",
    "RandomSkillChoiceResolver",
    "AnySkillChoiceResolver",
]
