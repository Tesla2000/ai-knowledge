from random import randint
from typing import Annotated

from pydantic import AfterValidator, Field, PositiveInt

from dnd.character._creature_base import _CreatureBase
from dnd.fight._action_group import _And, _Or, _Action


def _roll_initiative(data: dict[str, object]) -> int:
    initiative_bonus = data.get("initiative_bonus", 0)
    if not isinstance(initiative_bonus, int):
        raise ValueError(f"initiative_bonus must be int, got {type(initiative_bonus)}")
    return randint(1, 20) + initiative_bonus


def _default_type(data: dict[str, object]) -> str:
    name = data["name"]
    if not isinstance(name, str):
        raise ValueError(f"name must be str, got {type(name)}")
    return name


def _require_attacks(
    attacks: tuple[_Action | _Or | _And, ...],
) -> tuple[_Action | _Or | _And, ...]:
    if not attacks:
        raise ValueError("creature must have at least one attack")
    return attacks


_Attacks = Annotated[tuple[_Action | _Or | _And, ...], AfterValidator(_require_attacks)]


class _Creature(_CreatureBase):
    initiative: PositiveInt = Field(default_factory=_roll_initiative)
    type: str = Field(default_factory=_default_type)
    attacks: _Attacks


class _PlayerFightCreature(_CreatureBase):
    initiative: int
