from __future__ import annotations

from dnd.choices.abilities.ActionType import ActionType
from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


class Ability(BaseModel):
    model_config = ConfigDict(validate_by_alias=True, validate_by_name=True)

    name: str = ""
    action_type: ActionType = Field(
        description="Free action if not provided.",
        validation_alias="ability_type",
        exclude=True,
    )
    combat_related: bool = Field(
        description="Does this ability posses utility in combat. Mostly yes, "
        "the exceptions are improvements to skills parameters, "
        "and abilities such as trans or increased carrying "
        "capacity. Examples pack tactics, sunlite sensitivity.",
        default=True,
    )
    spell_grant: bool = Field(
        description="This ability allows of a use of a spell",
        default=False,
        exclude=True,
    )
    description: str
    required_level: int = Field(
        description="If more than one value is provided pick the lowest.",
        default=0,
        exclude=True,
    )
