"""Base class for assigning a single CharacterData field."""

from abc import ABC
from abc import abstractmethod

from dnd.character.blueprint.building_blocks.building_block import BuildingBlock
from dnd.character.blueprint.character_data import CharacterData
from typing import TypeVar

from dnd.character.blueprint.sentinels import (
    _ARK,
    _BAK,
    _BDK,
    _CLK,
    _DRK,
    _FGK,
    _HeK,
    _MOK,
    _PAK,
    _RAK,
    _ROK,
    _RK,
    _SOK,
    _SkCK,
    _StCK,
    _StK,
    _WAK,
    AnyWizardLevel,
)
from dnd.character.blueprint.states._caster_info import CasterInfo
from dnd.character.blueprint.states.state import Blueprint
from dnd.character.blueprint.states.wizard._info import WizardInfo

_WIK = TypeVar("_WIK", bound=WizardInfo[AnyWizardLevel] | None)
_CK = TypeVar("_CK", bound=CasterInfo | None)


class CharacterDataFieldAssigner(BuildingBlock, ABC):
    """Abstract base for building blocks that update one field inside CharacterData."""

    @abstractmethod
    def _update(self, character_data: CharacterData) -> CharacterData: ...

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
            CharacterData,
        ],
    ) -> Blueprint[
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
        CharacterData,
    ]:
        return blueprint.model_copy(
            update={"character_data": self._update(blueprint.character_data)}
        )
