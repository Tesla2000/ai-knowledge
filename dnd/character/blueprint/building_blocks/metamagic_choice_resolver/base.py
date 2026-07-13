from abc import ABC
from abc import abstractmethod

from dnd.character.blueprint.building_blocks.building_block import BuildingBlock
from dnd.character.blueprint.sentinels import AnyClassLevel
from dnd.character.blueprint.sentinels import AnyMetamagicChoices
from dnd.character.blueprint.sentinels import AnySorcererLevel
from dnd.character.blueprint.sentinels import AnyStatChoices
from dnd.character.blueprint.sentinels import AnyWizardLevel
from dnd.character.blueprint.sentinels import MaybeCharacterData
from dnd.character.blueprint.states.sorcerer.base import AnySorcererBlueprint
from dnd.character.blueprint.states.sorcerer.base import SorcererBlueprint
from dnd.character.blueprint.states.sorcerer.presentable import (
    PresentableSorcererBlueprint,
)
from dnd.choices.abilities.metamagic import MetamagicOption


class MetamagicChoiceResolver(BuildingBlock, ABC):
    """Abstract base for resolving n_metamagic_choices into metamagic_options."""

    @abstractmethod
    def _select_metamagic(
        self, state: AnySorcererBlueprint, n: int
    ) -> tuple[MetamagicOption, ...]: ...

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
        _McK_: AnyMetamagicChoices,
    ](
        self,
        blueprint: SorcererBlueprint[
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
            _McK_,
        ],
    ) -> PresentableSorcererBlueprint[
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
        if blueprint.n_metamagic_choices == 0:
            return PresentableSorcererBlueprint[
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
        selected = self._select_metamagic(blueprint, blueprint.n_metamagic_choices)
        return PresentableSorcererBlueprint[
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
                "metamagic_options": blueprint.metamagic_options + selected,
                "n_metamagic_choices": 0,
            }
        )
