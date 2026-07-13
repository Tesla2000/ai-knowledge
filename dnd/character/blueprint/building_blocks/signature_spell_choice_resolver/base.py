from abc import ABC
from abc import abstractmethod

from dnd.character.blueprint.building_blocks.building_block import BuildingBlock
from dnd.character.blueprint.sentinels import AnyClassLevel
from dnd.character.blueprint.sentinels import AnySorcererLevel
from dnd.character.blueprint.sentinels import AnySignatureSpellChoices
from dnd.character.blueprint.sentinels import AnyStatChoices
from dnd.character.blueprint.sentinels import AnyWizardLevel
from dnd.character.blueprint.sentinels import MaybeCharacterData
from dnd.character.blueprint.states.wizard.level20 import AnyWizardLevel20Blueprint
from dnd.character.blueprint.states.wizard.level20 import WizardLevel20Blueprint
from dnd.character.blueprint.states.wizard.presentable import (
    PresentableWizardLevel20Blueprint,
)
from dnd.character.spells.spell_slots import Spell


class SignatureSpellChoiceResolver(BuildingBlock, ABC):
    """Abstract base for resolving n_signature_spell_choices into signature_spells."""

    @abstractmethod
    def _select_signature_spells(
        self, state: AnyWizardLevel20Blueprint, n: int
    ) -> tuple[Spell, ...]: ...

    def apply[
        _StCK_: AnyStatChoices,
        _SkCK_: AnyStatChoices,
        _WZK_: AnyWizardLevel,
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
        _SigK_: AnySignatureSpellChoices,
    ](
        self,
        blueprint: WizardLevel20Blueprint[
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
            _SigK_,
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
        if blueprint.n_signature_spell_choices == 0:
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
            blueprint, blueprint.n_signature_spell_choices
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
        ].model_validate(
            dict(blueprint)
            | {
                "signature_spells": blueprint.signature_spells + selected,
                "n_signature_spell_choices": 0,
            }
        )
