from abc import ABC
from abc import abstractmethod
from typing import assert_never

from dnd.character.blueprint.building_blocks.building_block import BuildingBlock
from dnd.character.blueprint.states.state import Blueprint
from dnd.character.blueprint.sentinels import (
    _RK,
    _StK,
    _HeK,
    _StCK,
    _SkCK,
    _WZK,
    _SOK,
    _FGK,
    _BAK,
    _ROK,
    _CLK,
    _DRK,
    _PAK,
    _RAK,
    _MOK,
    _BDK,
    _WAK,
    _ARK,
    _CDK,
)
from dnd.choices.class_creation.character_class import Class
from dnd.choices.equipment_creation.weapons import HitDieSize
from pydantic import Field
from pydantic import PositiveInt


class HealthIncrease(BuildingBlock, ABC):
    """Abstract base class for health increase strategies when leveling up.

    Subclasses must implement _get_hit_die_value to determine how much
    health to gain from the hit die (fixed value, random roll, etc.).
    """

    class_: Class = Field(
        description="The character class for which health is being increased"
    )

    @classmethod
    def _class_hit_die(cls, class_: Class) -> HitDieSize:
        match class_:
            case Class.BARBARIAN:
                return HitDieSize.TWELVE
            case Class.FIGHTER | Class.PALADIN | Class.RANGER:
                return HitDieSize.TEN
            case Class.SORCERER | Class.WIZARD:
                return HitDieSize.SIX
            case (
                Class.BARD
                | Class.CLERIC
                | Class.DRUID
                | Class.MONK
                | Class.ROGUE
                | Class.WARLOCK
                | Class.ARTIFICER
            ):
                return HitDieSize.EIGHT
            case _ as never:
                assert_never(never)

    @abstractmethod
    def _get_hit_die_value(self, hit_die: HitDieSize) -> int: ...

    def apply(
        self,
        blueprint: Blueprint[
            _RK,
            _StK,
            _HeK,
            _StCK,
            _SkCK,
            _WZK,
            _SOK,
            _FGK,
            _BAK,
            _ROK,
            _CLK,
            _DRK,
            _PAK,
            _RAK,
            _MOK,
            _BDK,
            _WAK,
            _ARK,
            _CDK,
        ],
    ) -> Blueprint[
        _RK,
        _StK,
        PositiveInt,
        _StCK,
        _SkCK,
        _WZK,
        _SOK,
        _FGK,
        _BAK,
        _ROK,
        _CLK,
        _DRK,
        _PAK,
        _RAK,
        _MOK,
        _BDK,
        _WAK,
        _ARK,
        _CDK,
    ]:
        hit_die = self._class_hit_die(self.class_)
        if blueprint.health_base is None:
            hit_die_value = hit_die.value
            base_health: int = 0
        else:
            hit_die_value = self._get_hit_die_value(hit_die)
            base_health = blueprint.health_base

        return Blueprint[
            _RK,
            _StK,
            PositiveInt,
            _StCK,
            _SkCK,
            _WZK,
            _SOK,
            _FGK,
            _BAK,
            _ROK,
            _CLK,
            _DRK,
            _PAK,
            _RAK,
            _MOK,
            _BDK,
            _WAK,
            _ARK,
            _CDK,
        ].model_validate(dict(blueprint) | {"health_base": base_health + hit_die_value})
