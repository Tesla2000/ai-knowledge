from __future__ import annotations

from typing import Literal

from dnd.character.spells.spell_slots import Cantrip
from dnd.character.spells.spell_slots import EighthLevel
from dnd.character.spells.spell_slots import FifthLevel
from dnd.character.spells.spell_slots import FirstLevel
from dnd.character.spells.spell_slots import FourthLevel
from dnd.character.spells.spell_slots import NinthLevel
from dnd.character.spells.spell_slots import SecondLevel
from dnd.character.spells.spell_slots import SeventhLevel
from dnd.character.spells.spell_slots import SixthLevel
from dnd.character.spells.spell_slots import Spell
from dnd.character.spells.spell_slots import ThirdLevel
from pydantic import BaseModel
from pydantic import Field

_INDEX = "index"


class Spells(BaseModel):
    cantrips: tuple[Cantrip, ...] = Field(
        default_factory=tuple, json_schema_extra={_INDEX: 0}
    )
    first_level_spells: tuple[FirstLevel, ...] = Field(
        default_factory=tuple, json_schema_extra={_INDEX: 1}
    )
    second_level_spells: tuple[SecondLevel, ...] = Field(
        default_factory=tuple, json_schema_extra={_INDEX: 2}
    )
    third_level_spells: tuple[ThirdLevel, ...] = Field(
        default_factory=tuple, json_schema_extra={_INDEX: 3}
    )
    fourth_level_spells: tuple[FourthLevel, ...] = Field(
        default_factory=tuple, json_schema_extra={_INDEX: 4}
    )
    fifth_level_spells: tuple[FifthLevel, ...] = Field(
        default_factory=tuple, json_schema_extra={_INDEX: 5}
    )
    sixth_level_spells: tuple[SixthLevel, ...] = Field(
        default_factory=tuple, json_schema_extra={_INDEX: 6}
    )
    seventh_level_spells: tuple[SeventhLevel, ...] = Field(
        default_factory=tuple, json_schema_extra={_INDEX: 7}
    )
    eighth_level_spells: tuple[EighthLevel, ...] = Field(
        default_factory=tuple, json_schema_extra={_INDEX: 8}
    )
    ninth_level_spells: tuple[NinthLevel, ...] = Field(
        default_factory=tuple, json_schema_extra={_INDEX: 9}
    )

    def get_spells_by_level(self) -> tuple[tuple[Spell, ...]]:
        return Spells.model_dump(self).values()

    def get_spell_level_by_index(
        self, index: Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    ) -> tuple[Spell, ...]:
        return next(
            getattr(self, field_name)
            for field_name, field_info in type(self).model_fields.items()
            if field_info.json_schema_extra[_INDEX] == index
        )
