from __future__ import annotations

from typing import NamedTuple, cast

from dnd.character.spells.spell_slots import SpellLevel


class SpellSlots(NamedTuple):
    level_1: int
    level_2: int
    level_3: int
    level_4: int
    level_5: int
    level_6: int
    level_7: int
    level_8: int
    level_9: int

    def spend_level_1_slot(self) -> SpellSlots:
        if self.level_1 == 0:
            raise ValueError("No level-1 spell slots remaining")
        return self._replace(level_1=self.level_1 - 1)

    def spend_level_2_slot(self) -> SpellSlots:
        if self.level_2 == 0:
            raise ValueError("No level-2 spell slots remaining")
        return self._replace(level_2=self.level_2 - 1)

    def spend_level_3_slot(self) -> SpellSlots:
        if self.level_3 == 0:
            raise ValueError("No level-3 spell slots remaining")
        return self._replace(level_3=self.level_3 - 1)

    def spend_level_4_slot(self) -> SpellSlots:
        if self.level_4 == 0:
            raise ValueError("No level-4 spell slots remaining")
        return self._replace(level_4=self.level_4 - 1)

    def spend_level_5_slot(self) -> SpellSlots:
        if self.level_5 == 0:
            raise ValueError("No level-5 spell slots remaining")
        return self._replace(level_5=self.level_5 - 1)

    def spend_level_6_slot(self) -> SpellSlots:
        if self.level_6 == 0:
            raise ValueError("No level-6 spell slots remaining")
        return self._replace(level_6=self.level_6 - 1)

    def spend_level_7_slot(self) -> SpellSlots:
        if self.level_7 == 0:
            raise ValueError("No level-7 spell slots remaining")
        return self._replace(level_7=self.level_7 - 1)

    def spend_level_8_slot(self) -> SpellSlots:
        if self.level_8 == 0:
            raise ValueError("No level-8 spell slots remaining")
        return self._replace(level_8=self.level_8 - 1)

    def spend_level_9_slot(self) -> SpellSlots:
        if self.level_9 == 0:
            raise ValueError("No level-9 spell slots remaining")
        return self._replace(level_9=self.level_9 - 1)

    def max_level(self) -> SpellLevel:
        for i in range(8, -1, -1):
            if self[i] > 0:
                return cast(SpellLevel, i + 1)
        return 0


FULL_CASTER_SPELL_SLOTS: tuple[SpellSlots, ...] = (
    SpellSlots(2, 0, 0, 0, 0, 0, 0, 0, 0),
    SpellSlots(3, 0, 0, 0, 0, 0, 0, 0, 0),
    SpellSlots(4, 2, 0, 0, 0, 0, 0, 0, 0),
    SpellSlots(4, 3, 0, 0, 0, 0, 0, 0, 0),
    SpellSlots(4, 3, 2, 0, 0, 0, 0, 0, 0),
    SpellSlots(4, 3, 3, 0, 0, 0, 0, 0, 0),
    SpellSlots(4, 3, 3, 1, 0, 0, 0, 0, 0),
    SpellSlots(4, 3, 3, 2, 0, 0, 0, 0, 0),
    SpellSlots(4, 3, 3, 3, 1, 0, 0, 0, 0),
    SpellSlots(4, 3, 3, 3, 2, 0, 0, 0, 0),
    SpellSlots(4, 3, 3, 3, 2, 1, 0, 0, 0),
    SpellSlots(4, 3, 3, 3, 2, 1, 0, 0, 0),
    SpellSlots(4, 3, 3, 3, 2, 1, 1, 0, 0),
    SpellSlots(4, 3, 3, 3, 2, 1, 1, 0, 0),
    SpellSlots(4, 3, 3, 3, 2, 1, 1, 1, 0),
    SpellSlots(4, 3, 3, 3, 2, 1, 1, 1, 0),
    SpellSlots(4, 3, 3, 3, 2, 1, 1, 1, 1),
    SpellSlots(4, 3, 3, 3, 3, 1, 1, 1, 1),
    SpellSlots(4, 3, 3, 3, 3, 2, 1, 1, 1),
    SpellSlots(4, 3, 3, 3, 3, 2, 2, 1, 1),
)
