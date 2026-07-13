from typing import ClassVar
from typing import Generic
from typing import Literal

from pydantic import ConfigDict

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
from dnd.character.blueprint.sentinels import _WZK_co
from dnd.character.blueprint.states.convertible_blueprint import ConvertibleBlueprint
from dnd.character.blueprint.states.sorcerer.base import SorcererBlueprint
from dnd.character.presentable_character import PresentableCharacter


class PresentableSorcererBlueprint(
    SorcererBlueprint[
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
        Literal[0],
    ],
    ConvertibleBlueprint,
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
    ],
):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    def to_presentable_character(self) -> PresentableCharacter:
        return PresentableCharacter.model_validate(dict(self))
