from typing import ClassVar
from typing import Generic
from typing import cast

from pydantic import ConfigDict
from pydantic import Field

from dnd.character.blueprint.sentinels import AnyClassLevel
from dnd.character.blueprint.sentinels import AnySorcererLevel
from dnd.character.blueprint.sentinels import AnySignatureSpellChoices
from dnd.character.blueprint.sentinels import AnyStatChoices
from dnd.character.blueprint.sentinels import AnyWizardLevel
from dnd.character.blueprint.sentinels import MaybeCharacterData
from dnd.character.blueprint.sentinels import _ARK_co
from dnd.character.blueprint.sentinels import _BAK_co
from dnd.character.blueprint.sentinels import _BDK_co
from dnd.character.blueprint.sentinels import _CDK_co
from dnd.character.blueprint.sentinels import _CLK_co
from dnd.character.blueprint.sentinels import _DRK_co
from dnd.character.blueprint.sentinels import _FGK_co
from dnd.character.blueprint.sentinels import _MOK_co
from dnd.character.blueprint.sentinels import _PAK_co
from dnd.character.blueprint.sentinels import _RAK_co
from dnd.character.blueprint.sentinels import _ROK_co
from dnd.character.blueprint.sentinels import _SigK_co
from dnd.character.blueprint.sentinels import _SkCK_co
from dnd.character.blueprint.sentinels import _SOK_co
from dnd.character.blueprint.sentinels import _StCK_co
from dnd.character.blueprint.sentinels import _WAK_co
from dnd.character.blueprint.sentinels import _WZK_co
from dnd.character.blueprint.states.wizard.level18 import WizardLevel18Blueprint
from dnd.character.spells.spell_slots import Spell


class WizardLevel20Blueprint(
    WizardLevel18Blueprint[
        _StCK_co,
        _SkCK_co,
        _WZK_co,
        _SOK_co,
        _FGK_co,
        _BAK_co,
        _ROK_co,
        _CLK_co,
        _DRK_co,
        _PAK_co,
        _RAK_co,
        _MOK_co,
        _BDK_co,
        _WAK_co,
        _ARK_co,
        _CDK_co,
    ],
    Generic[
        _StCK_co,
        _SkCK_co,
        _WZK_co,
        _SOK_co,
        _FGK_co,
        _BAK_co,
        _ROK_co,
        _CLK_co,
        _DRK_co,
        _PAK_co,
        _RAK_co,
        _MOK_co,
        _BDK_co,
        _WAK_co,
        _ARK_co,
        _CDK_co,
        _SigK_co,
    ],
):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    signature_spells: tuple[Spell, ...] = Field(default=())
    n_signature_spell_choices: _SigK_co = Field(default=cast(_SigK_co, 0))


type AnyWizardLevel20Blueprint = WizardLevel20Blueprint[
    AnyStatChoices,
    AnyStatChoices,
    AnyWizardLevel,
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
    AnySignatureSpellChoices,
]
