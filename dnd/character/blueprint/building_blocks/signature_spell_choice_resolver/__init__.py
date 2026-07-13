from typing import Annotated
from typing import Union

from pydantic import Field

from dnd.character.blueprint.building_blocks.signature_spell_choice_resolver.base import (
    SignatureSpellChoiceResolver,
)
from dnd.character.blueprint.building_blocks.signature_spell_choice_resolver.random import (
    RandomSignatureSpellChoiceResolver,
)

AnySignatureSpellChoiceResolver = Annotated[
    Union[RandomSignatureSpellChoiceResolver,],
    Field(discriminator="type"),
]

__all__ = [
    "SignatureSpellChoiceResolver",
    "RandomSignatureSpellChoiceResolver",
    "AnySignatureSpellChoiceResolver",
]
