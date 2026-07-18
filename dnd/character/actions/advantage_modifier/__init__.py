from typing import Annotated, Union

from pydantic import Field

from dnd.character.actions.advantage_modifier._base import (
    _AdvantageModifier as AdvantageModifier,
    _DisadvantageModifier as DisadvantageModifier,
    _GrantsAdvantageModifier as GrantsAdvantageModifier,
)
from dnd.character.actions.advantage_modifier._reckless import (
    _RecklessAdvantageModifier as RecklessAdvantageModifier,
    _RecklessGrantsAdvantageModifier as RecklessGrantsAdvantageModifier,
)
from dnd.character.actions.advantage_modifier._type import AdvantageModifierType

AnyAdvantageModifier = Annotated[
    Union[RecklessAdvantageModifier, RecklessGrantsAdvantageModifier],
    Field(discriminator="type"),
]

__all__ = [
    "AdvantageModifier",
    "AdvantageModifierType",
    "AnyAdvantageModifier",
    "DisadvantageModifier",
    "GrantsAdvantageModifier",
    "RecklessAdvantageModifier",
    "RecklessGrantsAdvantageModifier",
]
