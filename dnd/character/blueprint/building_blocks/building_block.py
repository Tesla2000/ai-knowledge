from __future__ import annotations

from abc import abstractmethod
from collections.abc import Generator

from dnd.character.blueprint.state import BlueprintProtocol
from dnd.character.delta.delta import Delta
from pydantic import BaseModel
from pydantic import ConfigDict


class BuildingBlock(BaseModel):
    """Abstract base for a pipeline step that yields deltas and returns new state."""

    model_config = ConfigDict(frozen=True)

    @abstractmethod
    def get_change[T: BlueprintProtocol](
        self, state: T
    ) -> Generator[Delta, None, BlueprintProtocol]:
        raise NotImplementedError(f"{type(self).__name__} must implement get_change")

    def flatten(self) -> Generator[BuildingBlock]:
        yield self
