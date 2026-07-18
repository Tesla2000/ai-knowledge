from typing import ClassVar
from typing import Generic

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field

from dnd.character.blueprint.sentinels import _WZK_co
from dnd.character.spells.spell_slots import Spell


class WizardInfo(BaseModel, Generic[_WZK_co]):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    prepared_spells: tuple[Spell, ...] = Field(default=())


class WizardLevel18Info(WizardInfo[_WZK_co], Generic[_WZK_co]):
    spell_mastery_spells: tuple[Spell, ...] = Field(default=())


class WizardLevel20Info(WizardLevel18Info[_WZK_co], Generic[_WZK_co]):
    signature_spells: tuple[Spell, ...] = Field(default=())
    n_signature_spell_choices: int = 0
