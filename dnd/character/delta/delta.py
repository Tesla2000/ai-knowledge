from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING

from dnd.character.blueprint.state import BlueprintProtocol
from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import computed_field


class Delta(BaseModel):
    model_config = ConfigDict(frozen=True)

    if TYPE_CHECKING:

        @property
        def delta_type(self) -> str:
            return type(self).__name__

    else:

        @computed_field
        @property
        def delta_type(self) -> str:
            return type(self).__name__

    @abstractmethod
    def apply(self, state: BlueprintProtocol) -> BlueprintProtocol: ...
