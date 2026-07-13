"""Base class for assigning a single CharacterData field."""

from abc import ABC
from abc import abstractmethod

from dnd.character.blueprint.building_blocks.building_block import BuildingBlock
from dnd.character.blueprint.character_data import CharacterData
from dnd.character.blueprint.states.state import _BPT
from pydantic import ConfigDict


class CharacterDataFieldAssigner(BuildingBlock, ABC):
    """Abstract base for building blocks that update one field inside CharacterData."""

    model_config = ConfigDict(frozen=True)

    @abstractmethod
    def _update(self, character_data: CharacterData) -> CharacterData: ...

    def apply(self, blueprint: _BPT) -> _BPT:
        cd = blueprint.character_data or CharacterData()
        return blueprint.model_copy(update={"character_data": self._update(cd)})
