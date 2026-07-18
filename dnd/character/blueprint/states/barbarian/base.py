from typing import ClassVar
from typing import Generic
from typing import TypeVar

from pydantic import ConfigDict
from pydantic import PositiveInt

from dnd.character.blueprint.sentinels import AnyWizardLevel
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
from dnd.character.blueprint.sentinels import _SkCK_co
from dnd.character.blueprint.sentinels import _SOK_co
from dnd.character.blueprint.sentinels import _StCK_co
from dnd.character.blueprint.sentinels import _WAK_co
from dnd.character.blueprint.states._caster_info import CasterInfo
from dnd.character.blueprint.states.state import Blueprint
from dnd.character.blueprint.states.wizard._info import WizardInfo
from dnd.character.race.race import Race
from dnd.character.stats import Stats

_WIK_co = TypeVar("_WIK_co", bound=WizardInfo[AnyWizardLevel] | None, covariant=True)
_CK_co = TypeVar("_CK_co", bound=CasterInfo | None, covariant=True)


class BarbarianBlueprint(
    Blueprint[
        Race,
        Stats,
        PositiveInt,
        _StCK_co,
        _SkCK_co,
        _WIK_co,
        _CK_co,
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
        _WIK_co,
        _CK_co,
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
):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)
