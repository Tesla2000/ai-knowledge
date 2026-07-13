"""Optional character identity/flavor data, assigned incrementally by building blocks."""

from typing import ClassVar

from dnd.choices.alignment import Alignment
from dnd.choices.background_creatrion.background import Background
from dnd.choices.sex import Sex
from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import PositiveInt


class CharacterData(BaseModel):
    """Flat bag of optional character identity/flavor fields.

    Mirrors the corresponding fields on Character, but all optional so it can
    be filled in incrementally by building blocks (e.g. AgeAssigner sets only
    `age`).
    """

    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    name: str | None = None
    sex: Sex | None = None
    age: PositiveInt | None = None
    background: Background | None = None
    alignment: Alignment | None = None
    backstory: str | None = None
    height: PositiveInt | None = None
    weight: PositiveInt | None = None
    eye_color: str | None = None
    skin_color: str | None = None
    hairstyle: str | None = None
    appearance: str | None = None
    character_traits: str | None = None
    ideals: str | None = None
    bonds: str | None = None
    weaknesses: str | None = None
