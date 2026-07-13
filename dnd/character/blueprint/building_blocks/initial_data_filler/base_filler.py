from abc import ABC
from abc import abstractmethod

from dnd.character.blueprint.building_blocks.building_block import BuildingBlock
from dnd.character.blueprint.building_blocks.building_block import _WideBlueprint
from dnd.character.blueprint.character_data import CharacterData
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
    _RK,
    _ROK,
    _SkCK,
    _SOK,
    _StCK,
    _StK,
    _WAK,
    _WZK,
)
from dnd.character.blueprint.states.state import Blueprint
from pydantic import ConfigDict


class InitialDataFiller(BuildingBlock, ABC):
    model_config = ConfigDict(frozen=True)

    @abstractmethod
    def compute_character_data(self, blueprint: _WideBlueprint) -> CharacterData: ...

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
            None,
        ],
    ) -> Blueprint[
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
        CharacterData,
    ]:
        return Blueprint[
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
            CharacterData,
        ].model_validate(
            dict(blueprint) | {"character_data": self.compute_character_data(blueprint)}
        )
