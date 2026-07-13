from typing import Annotated
from typing import ClassVar
from typing import Literal

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from pydantic import PositiveInt

from dnd.choices.abilities.action_type import ActionType
from dnd.choices.stats_creation.statistic import Statistic


class BasicAction(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    type: Literal["basic"] = "basic"
    action_type: ActionType
    name: str
    description: str


class AttackAction(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    type: Literal["attack"] = "attack"
    action_type: ActionType
    name: str
    description: str
    n_dice: PositiveInt
    dice_size: PositiveInt
    attack_bonus: int = 0
    damage_bonus: int = 0


class SavingThrowAction(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    type: Literal["saving_throw"] = "saving_throw"
    action_type: ActionType
    name: str
    description: str
    n_dice: PositiveInt
    dice_size: PositiveInt
    dc: int
    saving_throw_type: Statistic
    half_on_success: bool = True


AnyLeafAction = Annotated[
    BasicAction | AttackAction | SavingThrowAction,
    Field(discriminator="type"),
]


class OrAction(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    type: Literal["or"] = "or"
    action_type: ActionType
    name: str
    description: str
    options: tuple[AnyLeafAction, ...]


class AndAction(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    type: Literal["and"] = "and"
    action_type: ActionType
    name: str
    description: str
    options: tuple[AnyLeafAction, ...]


AnyAction = Annotated[
    BasicAction | AttackAction | SavingThrowAction | OrAction | AndAction,
    Field(discriminator="type"),
]
