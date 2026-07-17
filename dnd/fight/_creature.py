from collections.abc import Mapping
from random import randint
from typing import Annotated

from pydantic import AfterValidator, Field, PositiveInt

from dnd.character._creature_base import _CreatureBase
from dnd.character.stats import Stats
from dnd.fight._action_group import _And, _Or, _Action
from dnd.fight._non_attack import _NonAttack


def _default_hp(data: Mapping[str, object]) -> int:  # ignore
    stats = data.get("stats")
    constitution = 10
    if isinstance(stats, Stats):
        constitution = stats.constitution
    elif stats is not None:
        raise TypeError(f"stats must be Stats, got {type(stats)}")
    con_mod = (constitution - 10) // 2
    n_raw = data.get("n_hit_dice", 1)
    d_raw = data.get("hit_die_size", 8)
    n = n_raw if isinstance(n_raw, int) else 1
    d = d_raw if isinstance(d_raw, int) else 8
    return max(1, n * (d + 1) // 2 + con_mod * n)


def _roll_initiative(data: Mapping[str, object]) -> int:  # ignore
    initiative_bonus = data.get("initiative_bonus", 0)
    if not isinstance(initiative_bonus, int):
        raise ValueError(f"initiative_bonus must be int, got {type(initiative_bonus)}")
    return randint(1, 20) + initiative_bonus


def _default_type(data: Mapping[str, object]) -> str:  # ignore
    name = data["name"]
    if not isinstance(name, str):
        raise ValueError(f"name must be str, got {type(name)}")
    return name


def _require_attacks(
    attacks: tuple[_Action | _NonAttack | _Or | _And, ...],
) -> tuple[_Action | _NonAttack | _Or | _And, ...]:
    if not attacks:
        raise ValueError("creature must have at least one attack")
    return attacks


_Attacks = Annotated[
    tuple[_Action | _NonAttack | _Or | _And, ...], AfterValidator(_require_attacks)
]


class _Creature(_CreatureBase):
    initiative: PositiveInt = Field(default_factory=_roll_initiative)
    type: str = Field(default_factory=_default_type)
    attacks: _Attacks
    n_hit_dice: PositiveInt
    hit_die_size: PositiveInt
    hp: PositiveInt = Field(default_factory=_default_hp)
