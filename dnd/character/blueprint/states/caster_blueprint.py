from typing import ClassVar
from typing import Self

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import NonNegativeInt

from dnd.character.spells.max_spell_levels import FULL_CASTER_SPELL_SLOTS
from dnd.character.spells.max_spell_levels import SpellSlots


class CasterBlueprint(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    spell_slots: SpellSlots
    caster_level: NonNegativeInt = 0

    def increase_full_caster(self) -> Self:
        new_level = self.caster_level + 1
        return self.model_copy(
            update={
                "caster_level": new_level,
                "spell_slots": FULL_CASTER_SPELL_SLOTS[new_level - 1],
            }
        )
