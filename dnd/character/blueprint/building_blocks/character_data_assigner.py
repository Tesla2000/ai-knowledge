"""Assigns a whole CharacterData object to the blueprint at once."""

from typing import Literal

from dnd.character.blueprint.building_blocks.building_block import BuildingBlock
from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)
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
    _ROK,
    _SOK,
    _StCK,
    _StK,
    _SkCK,
    _WAK,
    _RK,
    AnyWizardLevel,
)
from dnd.character.blueprint.states._caster_info import CasterInfo
from dnd.character.blueprint.states.state import Blueprint
from dnd.character.blueprint.states.wizard._info import WizardInfo
from typing import TypeVar

_WIK = TypeVar("_WIK", bound=WizardInfo[AnyWizardLevel] | None)
_CK = TypeVar("_CK", bound=CasterInfo | None)
from pydantic import ConfigDict
from pydantic import Field


class CharacterDataAssigner(BuildingBlock):
    """Assigns a whole CharacterData object to the blueprint at once.

    For deterministic/manual population, as an alternative to the AI/random
    fillers in initial_data_filler/. See CharacterDataFieldAssigner for
    assigning individual fields once character_data is already set.
    """

    model_config = ConfigDict(frozen=True)

    type: Literal[BuildingBlockType.CHARACTER_DATA_ASSIGNER] = (
        BuildingBlockType.CHARACTER_DATA_ASSIGNER
    )
    character_data: CharacterData = Field(
        description="Full character identity/flavor data to assign"
    )

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
            None,
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
        return Blueprint[
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
        ].model_validate(dict(blueprint) | {"character_data": self.character_data})
