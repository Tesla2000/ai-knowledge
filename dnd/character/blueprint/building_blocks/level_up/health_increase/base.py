from abc import ABC
from abc import abstractmethod
from typing import Generic
from typing import TypeVar
from typing import cast
from typing import get_args

from pydantic import PositiveInt

from dnd.character.blueprint.building_blocks.building_block import BuildingBlock
from dnd.character.blueprint.sentinels import (
    _RK,
    _StK,
    _HeK,
    _StCK,
    _SkCK,
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
    AnyWizardLevel,
)
from dnd.character.blueprint.states._caster_info import CasterInfo
from dnd.character.blueprint.states.state import Blueprint
from dnd.character.blueprint.states.wizard._info import WizardInfo
from dnd.choices.equipment_creation.weapons import HitDieSize

_WIK = TypeVar("_WIK", bound=WizardInfo[AnyWizardLevel] | None)
_CK = TypeVar("_CK", bound=CasterInfo | None)

_DH = TypeVar("_DH", bound=HitDieSize)


class HealthIncrease(BuildingBlock, Generic[_DH], ABC):
    """Abstract base class for health increase strategies when leveling up.

    Subclasses must implement _get_hit_die_value to determine how much
    health to gain from the hit die. The die size is encoded in the
    generic type parameter _DH.
    """

    @abstractmethod
    def _get_hit_die_value(self, hit_die: HitDieSize) -> int: ...

    def _die_size(self) -> HitDieSize:
        arg = type(self).__pydantic_generic_metadata__["args"][0]
        inner = get_args(arg)
        return cast(HitDieSize, inner[0] if inner else arg)

    def apply(
        self,
        blueprint: Blueprint[
            _RK,
            _StK,
            _HeK,
            _StCK,
            _SkCK,
            _WIK,
            _CK,
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
        _WIK,
        _CK,
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
        hit_die = self._die_size()
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
            _WIK,
            _CK,
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
