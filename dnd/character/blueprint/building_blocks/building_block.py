from pydantic import BaseModel
from pydantic import ConfigDict

from dnd.character.blueprint.sentinels import AnyClassLevel
from dnd.character.blueprint.sentinels import AnySorcererLevel
from dnd.character.blueprint.sentinels import AnyStatChoices
from dnd.character.blueprint.sentinels import AnyWizardLevel
from dnd.character.blueprint.sentinels import MaybeCharacterData
from dnd.character.blueprint.sentinels import MaybeHealth
from dnd.character.blueprint.sentinels import MaybeRace
from dnd.character.blueprint.sentinels import MaybeStats
from dnd.character.blueprint.states.state import Blueprint

_WideBlueprint = Blueprint[
    MaybeRace,
    MaybeStats,
    MaybeHealth,
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
]


class BuildingBlock(BaseModel):
    """Abstract base for a pipeline step that transforms blueprint state."""

    model_config = ConfigDict(frozen=True)
