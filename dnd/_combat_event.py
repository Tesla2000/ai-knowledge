from enum import StrEnum, auto
from typing import Annotated, Literal, Union

from pydantic import BaseModel, ConfigDict, Field
from uuid_string import UUIDString


class CombatEventType(StrEnum):
    RAGE_ENDS = auto()
    TURN_START = auto()
    TURN_END = auto()
    ROUND_START = auto()
    ROUND_END = auto()
    CREATURE_TARGETED = auto()
    CREATURE_ATTACKED = auto()
    MELEE_DAMAGE = auto()


class RageEndsEvent(BaseModel):
    model_config = ConfigDict(frozen=True)
    type: Literal[CombatEventType.RAGE_ENDS] = CombatEventType.RAGE_ENDS
    target_id: UUIDString


class TurnStartEvent(BaseModel):
    model_config = ConfigDict(frozen=True)
    type: Literal[CombatEventType.TURN_START] = CombatEventType.TURN_START
    target_id: UUIDString


class TurnEndEvent(BaseModel):
    model_config = ConfigDict(frozen=True)
    type: Literal[CombatEventType.TURN_END] = CombatEventType.TURN_END
    target_id: UUIDString


class RoundStartEvent(BaseModel):
    model_config = ConfigDict(frozen=True)
    type: Literal[CombatEventType.ROUND_START] = CombatEventType.ROUND_START


class RoundEndEvent(BaseModel):
    model_config = ConfigDict(frozen=True)
    type: Literal[CombatEventType.ROUND_END] = CombatEventType.ROUND_END


class CreatureTargetedEvent(BaseModel):
    model_config = ConfigDict(frozen=True)
    type: Literal[CombatEventType.CREATURE_TARGETED] = CombatEventType.CREATURE_TARGETED
    attacker_id: UUIDString
    defender_id: UUIDString
    attack_id: UUIDString


class CreatureAttackedEvent(BaseModel):
    model_config = ConfigDict(frozen=True)
    type: Literal[CombatEventType.CREATURE_ATTACKED] = CombatEventType.CREATURE_ATTACKED
    attacker_id: UUIDString
    defender_id: UUIDString
    roll: int
    total_bonus: int
    is_crit: bool
    attack_id: UUIDString


class MeleeDamageEvent(BaseModel):
    model_config = ConfigDict(frozen=True)
    type: Literal[CombatEventType.MELEE_DAMAGE] = CombatEventType.MELEE_DAMAGE
    attacker_id: UUIDString
    defender_id: UUIDString
    damage: int
    is_crit: bool
    attack_id: UUIDString


AnyCombatEvent = Annotated[
    Union[
        RageEndsEvent,
        TurnStartEvent,
        TurnEndEvent,
        RoundStartEvent,
        RoundEndEvent,
        CreatureTargetedEvent,
        CreatureAttackedEvent,
        MeleeDamageEvent,
    ],
    Field(discriminator="type"),
]

__all__ = [
    "AnyCombatEvent",
    "CombatEventType",
    "CreatureAttackedEvent",
    "CreatureTargetedEvent",
    "MeleeDamageEvent",
    "RageEndsEvent",
    "RoundEndEvent",
    "RoundStartEvent",
    "TurnEndEvent",
    "TurnStartEvent",
]
