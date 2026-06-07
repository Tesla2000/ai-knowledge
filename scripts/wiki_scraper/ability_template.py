from __future__ import annotations

from dnd.character.ability import Ability
from pydantic import BaseModel


class AbilitiesTemplate(BaseModel):
    abilities: list[Ability]
