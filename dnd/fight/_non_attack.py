from typing import ClassVar

from pydantic import BaseModel, ConfigDict


class _NonAttack(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    name: str = ""
    description: str

    def perform(self) -> str:
        return self.description
