from __future__ import annotations

from abc import abstractmethod

from dnd.character.blueprint.state import BlueprintProtocol
from pydantic import BaseModel
from pydantic import ConfigDict


class Delta(BaseModel):
    model_config = ConfigDict(frozen=True)

    @abstractmethod
    def apply(self, state: BlueprintProtocol) -> BlueprintProtocol: ...
