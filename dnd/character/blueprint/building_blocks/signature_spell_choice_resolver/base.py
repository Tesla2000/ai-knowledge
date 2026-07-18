from abc import ABC
from abc import abstractmethod

from dnd.character.blueprint.building_blocks.building_block import BuildingBlock
from dnd.character.blueprint.sentinels import AnyClassLevel
from dnd.character.blueprint.sentinels import AnySorcererLevel
from dnd.character.blueprint.sentinels import AnyStatChoices
from dnd.character.blueprint.sentinels import AnyWizardLevel
from dnd.character.blueprint.sentinels import MaybeCharacterData
from dnd.character.blueprint.sentinels import MaybeHealth
from dnd.character.blueprint.sentinels import MaybeRace
from dnd.character.blueprint.sentinels import MaybeStats
from dnd.character.blueprint.states._caster_info import CasterInfo
from dnd.character.blueprint.states.state import Blueprint
from dnd.character.blueprint.states.wizard._info import WizardLevel20Info
from dnd.character.blueprint.states.wizard.presentable import (
    PresentableWizardLevel20Blueprint,
)
from dnd.character.race.race import Race
from dnd.character.spells.spell_slots import Spell
from dnd.character.stats import Stats
from pydantic import PositiveInt

type AnyWizardLevel20Blueprint = Blueprint[
    MaybeRace,
    MaybeStats,
    MaybeHealth,
    AnyStatChoices,
    AnyStatChoices,
    WizardLevel20Info[AnyWizardLevel],
    CasterInfo,
    AnySorcererLevel,
    AnyClassLevel,
    AnyClassLevel,
    AnyClassLevel,
    AnyClassLevel,
    AnyClassLevel,
    AnyClassLevel,
    AnyClassLevel,
    AnyClassLevel,
    AnyClassLevel,
    AnyClassLevel,
    AnyClassLevel,
    MaybeCharacterData,
]


class SignatureSpellChoiceResolver(BuildingBlock, ABC):
    """Abstract base for resolving n_signature_spell_choices into signature_spells."""

    @abstractmethod
    def _select_signature_spells(
        self, state: AnyWizardLevel20Blueprint, n: int
    ) -> tuple[Spell, ...]: ...

    def apply[
        _WZK_: AnyWizardLevel,
        _StCK_: AnyStatChoices,
        _SkCK_: AnyStatChoices,
        _SOK_: AnySorcererLevel,
        _FGK_: AnyClassLevel,
        _BAK_: AnyClassLevel,
        _ROK_: AnyClassLevel,
        _CLK_: AnyClassLevel,
        _DRK_: AnyClassLevel,
        _PAK_: AnyClassLevel,
        _RAK_: AnyClassLevel,
        _MOK_: AnyClassLevel,
        _BDK_: AnyClassLevel,
        _WAK_: AnyClassLevel,
        _ARK_: AnyClassLevel,
        _CDK_: MaybeCharacterData,
    ](
        self,
        blueprint: Blueprint[
            Race,
            Stats,
            PositiveInt,
            _StCK_,
            _SkCK_,
            WizardLevel20Info[_WZK_],
            CasterInfo,
            _SOK_,
            _FGK_,
            _BAK_,
            _ROK_,
            _CLK_,
            _DRK_,
            _PAK_,
            _RAK_,
            _MOK_,
            _BDK_,
            _WAK_,
            _ARK_,
            _CDK_,
        ],
    ) -> PresentableWizardLevel20Blueprint[
        _StCK_,
        _SkCK_,
        _WZK_,
        _SOK_,
        _FGK_,
        _BAK_,
        _ROK_,
        _CLK_,
        _DRK_,
        _PAK_,
        _RAK_,
        _MOK_,
        _BDK_,
        _WAK_,
        _ARK_,
        _CDK_,
    ]:
        if blueprint.wizard.n_signature_spell_choices == 0:
            return PresentableWizardLevel20Blueprint[
                _StCK_,
                _SkCK_,
                _WZK_,
                _SOK_,
                _FGK_,
                _BAK_,
                _ROK_,
                _CLK_,
                _DRK_,
                _PAK_,
                _RAK_,
                _MOK_,
                _BDK_,
                _WAK_,
                _ARK_,
                _CDK_,
            ].model_validate(dict(blueprint))
        selected = self._select_signature_spells(
            blueprint, blueprint.wizard.n_signature_spell_choices
        )
        updated_wizard = blueprint.wizard.model_copy(
            update={
                "signature_spells": blueprint.wizard.signature_spells + selected,
                "n_signature_spell_choices": 0,
            }
        )
        return PresentableWizardLevel20Blueprint[
            _StCK_,
            _SkCK_,
            _WZK_,
            _SOK_,
            _FGK_,
            _BAK_,
            _ROK_,
            _CLK_,
            _DRK_,
            _PAK_,
            _RAK_,
            _MOK_,
            _BDK_,
            _WAK_,
            _ARK_,
            _CDK_,
        ].model_validate(dict(blueprint) | {"wizard": updated_wizard})
