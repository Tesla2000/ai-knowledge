from __future__ import annotations

from typing import Generic, Literal, NamedTuple, Never, TypeVar, cast, overload

from typing_extensions import deprecated

from dnd.character.spells.spell_slots import SpellLevel


_L1 = TypeVar("_L1", bound=int)
_L2 = TypeVar("_L2", bound=int)
_L3 = TypeVar("_L3", bound=int)
_L4 = TypeVar("_L4", bound=int)
_L5 = TypeVar("_L5", bound=int)
_L6 = TypeVar("_L6", bound=int)
_L7 = TypeVar("_L7", bound=int)
_L8 = TypeVar("_L8", bound=int)
_L9 = TypeVar("_L9", bound=int)


class SpellSlots(NamedTuple, Generic[_L1, _L2, _L3, _L4, _L5, _L6, _L7, _L8, _L9]):
    level_1: _L1
    level_2: _L2
    level_3: _L3
    level_4: _L4
    level_5: _L5
    level_6: _L6
    level_7: _L7
    level_8: _L8
    level_9: _L9

    # --- level 1 (max 4) ---

    @overload
    @deprecated("No level-1 spell slots remaining")
    def spend_level_1_slot(
        self: SpellSlots[Literal[0], _L2, _L3, _L4, _L5, _L6, _L7, _L8, _L9],
    ) -> Never: ...
    @overload
    def spend_level_1_slot(
        self: SpellSlots[Literal[1], _L2, _L3, _L4, _L5, _L6, _L7, _L8, _L9],
    ) -> SpellSlots[Literal[0], _L2, _L3, _L4, _L5, _L6, _L7, _L8, _L9]: ...
    @overload
    def spend_level_1_slot(
        self: SpellSlots[Literal[2], _L2, _L3, _L4, _L5, _L6, _L7, _L8, _L9],
    ) -> SpellSlots[Literal[1], _L2, _L3, _L4, _L5, _L6, _L7, _L8, _L9]: ...
    @overload
    def spend_level_1_slot(
        self: SpellSlots[Literal[3], _L2, _L3, _L4, _L5, _L6, _L7, _L8, _L9],
    ) -> SpellSlots[Literal[2], _L2, _L3, _L4, _L5, _L6, _L7, _L8, _L9]: ...
    @overload
    def spend_level_1_slot(
        self: SpellSlots[Literal[4], _L2, _L3, _L4, _L5, _L6, _L7, _L8, _L9],
    ) -> SpellSlots[Literal[3], _L2, _L3, _L4, _L5, _L6, _L7, _L8, _L9]: ...
    def spend_level_1_slot(
        self: SpellSlots[_L1, _L2, _L3, _L4, _L5, _L6, _L7, _L8, _L9],
    ) -> SpellSlots[_L1, _L2, _L3, _L4, _L5, _L6, _L7, _L8, _L9]:
        if self.level_1 == 0:
            raise ValueError("No level-1 spell slots remaining")
        return self._replace(level_1=self.level_1 - 1)

    # --- level 2 (max 3) ---

    @overload
    @deprecated("No level-2 spell slots remaining")
    def spend_level_2_slot(
        self: SpellSlots[_L1, Literal[0], _L3, _L4, _L5, _L6, _L7, _L8, _L9],
    ) -> Never: ...
    @overload
    def spend_level_2_slot(
        self: SpellSlots[_L1, Literal[1], _L3, _L4, _L5, _L6, _L7, _L8, _L9],
    ) -> SpellSlots[_L1, Literal[0], _L3, _L4, _L5, _L6, _L7, _L8, _L9]: ...
    @overload
    def spend_level_2_slot(
        self: SpellSlots[_L1, Literal[2], _L3, _L4, _L5, _L6, _L7, _L8, _L9],
    ) -> SpellSlots[_L1, Literal[1], _L3, _L4, _L5, _L6, _L7, _L8, _L9]: ...
    @overload
    def spend_level_2_slot(
        self: SpellSlots[_L1, Literal[3], _L3, _L4, _L5, _L6, _L7, _L8, _L9],
    ) -> SpellSlots[_L1, Literal[2], _L3, _L4, _L5, _L6, _L7, _L8, _L9]: ...
    def spend_level_2_slot(
        self: SpellSlots[_L1, _L2, _L3, _L4, _L5, _L6, _L7, _L8, _L9],
    ) -> SpellSlots[_L1, _L2, _L3, _L4, _L5, _L6, _L7, _L8, _L9]:
        if self.level_2 == 0:
            raise ValueError("No level-2 spell slots remaining")
        return self._replace(level_2=self.level_2 - 1)

    # --- level 3 (max 3) ---

    @overload
    @deprecated("No level-3 spell slots remaining")
    def spend_level_3_slot(
        self: SpellSlots[_L1, _L2, Literal[0], _L4, _L5, _L6, _L7, _L8, _L9],
    ) -> Never: ...
    @overload
    def spend_level_3_slot(
        self: SpellSlots[_L1, _L2, Literal[1], _L4, _L5, _L6, _L7, _L8, _L9],
    ) -> SpellSlots[_L1, _L2, Literal[0], _L4, _L5, _L6, _L7, _L8, _L9]: ...
    @overload
    def spend_level_3_slot(
        self: SpellSlots[_L1, _L2, Literal[2], _L4, _L5, _L6, _L7, _L8, _L9],
    ) -> SpellSlots[_L1, _L2, Literal[1], _L4, _L5, _L6, _L7, _L8, _L9]: ...
    @overload
    def spend_level_3_slot(
        self: SpellSlots[_L1, _L2, Literal[3], _L4, _L5, _L6, _L7, _L8, _L9],
    ) -> SpellSlots[_L1, _L2, Literal[2], _L4, _L5, _L6, _L7, _L8, _L9]: ...
    def spend_level_3_slot(
        self: SpellSlots[_L1, _L2, _L3, _L4, _L5, _L6, _L7, _L8, _L9],
    ) -> SpellSlots[_L1, _L2, _L3, _L4, _L5, _L6, _L7, _L8, _L9]:
        if self.level_3 == 0:
            raise ValueError("No level-3 spell slots remaining")
        return self._replace(level_3=self.level_3 - 1)

    # --- level 4 (max 3) ---

    @overload
    @deprecated("No level-4 spell slots remaining")
    def spend_level_4_slot(
        self: SpellSlots[_L1, _L2, _L3, Literal[0], _L5, _L6, _L7, _L8, _L9],
    ) -> Never: ...
    @overload
    def spend_level_4_slot(
        self: SpellSlots[_L1, _L2, _L3, Literal[1], _L5, _L6, _L7, _L8, _L9],
    ) -> SpellSlots[_L1, _L2, _L3, Literal[0], _L5, _L6, _L7, _L8, _L9]: ...
    @overload
    def spend_level_4_slot(
        self: SpellSlots[_L1, _L2, _L3, Literal[2], _L5, _L6, _L7, _L8, _L9],
    ) -> SpellSlots[_L1, _L2, _L3, Literal[1], _L5, _L6, _L7, _L8, _L9]: ...
    @overload
    def spend_level_4_slot(
        self: SpellSlots[_L1, _L2, _L3, Literal[3], _L5, _L6, _L7, _L8, _L9],
    ) -> SpellSlots[_L1, _L2, _L3, Literal[2], _L5, _L6, _L7, _L8, _L9]: ...
    def spend_level_4_slot(
        self: SpellSlots[_L1, _L2, _L3, _L4, _L5, _L6, _L7, _L8, _L9],
    ) -> SpellSlots[_L1, _L2, _L3, _L4, _L5, _L6, _L7, _L8, _L9]:
        if self.level_4 == 0:
            raise ValueError("No level-4 spell slots remaining")
        return self._replace(level_4=self.level_4 - 1)

    # --- level 5 (max 3) ---

    @overload
    @deprecated("No level-5 spell slots remaining")
    def spend_level_5_slot(
        self: SpellSlots[_L1, _L2, _L3, _L4, Literal[0], _L6, _L7, _L8, _L9],
    ) -> Never: ...
    @overload
    def spend_level_5_slot(
        self: SpellSlots[_L1, _L2, _L3, _L4, Literal[1], _L6, _L7, _L8, _L9],
    ) -> SpellSlots[_L1, _L2, _L3, _L4, Literal[0], _L6, _L7, _L8, _L9]: ...
    @overload
    def spend_level_5_slot(
        self: SpellSlots[_L1, _L2, _L3, _L4, Literal[2], _L6, _L7, _L8, _L9],
    ) -> SpellSlots[_L1, _L2, _L3, _L4, Literal[1], _L6, _L7, _L8, _L9]: ...
    @overload
    def spend_level_5_slot(
        self: SpellSlots[_L1, _L2, _L3, _L4, Literal[3], _L6, _L7, _L8, _L9],
    ) -> SpellSlots[_L1, _L2, _L3, _L4, Literal[2], _L6, _L7, _L8, _L9]: ...
    def spend_level_5_slot(
        self: SpellSlots[_L1, _L2, _L3, _L4, _L5, _L6, _L7, _L8, _L9],
    ) -> SpellSlots[_L1, _L2, _L3, _L4, _L5, _L6, _L7, _L8, _L9]:
        if self.level_5 == 0:
            raise ValueError("No level-5 spell slots remaining")
        return self._replace(level_5=self.level_5 - 1)

    # --- level 6 (max 2) ---

    @overload
    @deprecated("No level-6 spell slots remaining")
    def spend_level_6_slot(
        self: SpellSlots[_L1, _L2, _L3, _L4, _L5, Literal[0], _L7, _L8, _L9],
    ) -> Never: ...
    @overload
    def spend_level_6_slot(
        self: SpellSlots[_L1, _L2, _L3, _L4, _L5, Literal[1], _L7, _L8, _L9],
    ) -> SpellSlots[_L1, _L2, _L3, _L4, _L5, Literal[0], _L7, _L8, _L9]: ...
    @overload
    def spend_level_6_slot(
        self: SpellSlots[_L1, _L2, _L3, _L4, _L5, Literal[2], _L7, _L8, _L9],
    ) -> SpellSlots[_L1, _L2, _L3, _L4, _L5, Literal[1], _L7, _L8, _L9]: ...
    def spend_level_6_slot(
        self: SpellSlots[_L1, _L2, _L3, _L4, _L5, _L6, _L7, _L8, _L9],
    ) -> SpellSlots[_L1, _L2, _L3, _L4, _L5, _L6, _L7, _L8, _L9]:
        if self.level_6 == 0:
            raise ValueError("No level-6 spell slots remaining")
        return self._replace(level_6=self.level_6 - 1)

    # --- level 7 (max 2) ---

    @overload
    @deprecated("No level-7 spell slots remaining")
    def spend_level_7_slot(
        self: SpellSlots[_L1, _L2, _L3, _L4, _L5, _L6, Literal[0], _L8, _L9],
    ) -> Never: ...
    @overload
    def spend_level_7_slot(
        self: SpellSlots[_L1, _L2, _L3, _L4, _L5, _L6, Literal[1], _L8, _L9],
    ) -> SpellSlots[_L1, _L2, _L3, _L4, _L5, _L6, Literal[0], _L8, _L9]: ...
    @overload
    def spend_level_7_slot(
        self: SpellSlots[_L1, _L2, _L3, _L4, _L5, _L6, Literal[2], _L8, _L9],
    ) -> SpellSlots[_L1, _L2, _L3, _L4, _L5, _L6, Literal[1], _L8, _L9]: ...
    def spend_level_7_slot(
        self: SpellSlots[_L1, _L2, _L3, _L4, _L5, _L6, _L7, _L8, _L9],
    ) -> SpellSlots[_L1, _L2, _L3, _L4, _L5, _L6, _L7, _L8, _L9]:
        if self.level_7 == 0:
            raise ValueError("No level-7 spell slots remaining")
        return self._replace(level_7=self.level_7 - 1)

    # --- level 8 (max 1) ---

    @overload
    @deprecated("No level-8 spell slots remaining")
    def spend_level_8_slot(
        self: SpellSlots[_L1, _L2, _L3, _L4, _L5, _L6, _L7, Literal[0], _L9],
    ) -> Never: ...
    @overload
    def spend_level_8_slot(
        self: SpellSlots[_L1, _L2, _L3, _L4, _L5, _L6, _L7, Literal[1], _L9],
    ) -> SpellSlots[_L1, _L2, _L3, _L4, _L5, _L6, _L7, Literal[0], _L9]: ...
    def spend_level_8_slot(
        self: SpellSlots[_L1, _L2, _L3, _L4, _L5, _L6, _L7, _L8, _L9],
    ) -> SpellSlots[_L1, _L2, _L3, _L4, _L5, _L6, _L7, _L8, _L9]:
        if self.level_8 == 0:
            raise ValueError("No level-8 spell slots remaining")
        return self._replace(level_8=self.level_8 - 1)

    # --- level 9 (max 1) ---

    @overload
    @deprecated("No level-9 spell slots remaining")
    def spend_level_9_slot(
        self: SpellSlots[_L1, _L2, _L3, _L4, _L5, _L6, _L7, _L8, Literal[0]],
    ) -> Never: ...
    @overload
    def spend_level_9_slot(
        self: SpellSlots[_L1, _L2, _L3, _L4, _L5, _L6, _L7, _L8, Literal[1]],
    ) -> SpellSlots[_L1, _L2, _L3, _L4, _L5, _L6, _L7, _L8, Literal[0]]: ...
    def spend_level_9_slot(
        self: SpellSlots[_L1, _L2, _L3, _L4, _L5, _L6, _L7, _L8, _L9],
    ) -> SpellSlots[_L1, _L2, _L3, _L4, _L5, _L6, _L7, _L8, _L9]:
        if self.level_9 == 0:
            raise ValueError("No level-9 spell slots remaining")
        return self._replace(level_9=self.level_9 - 1)

    def max_level(self) -> SpellLevel:
        for i in range(8, -1, -1):
            if self[i] > 0:
                return cast(SpellLevel, i + 1)
        return cast(SpellLevel, 0)


FULL_CASTER_SPELL_SLOTS: tuple[
    SpellSlots[int, int, int, int, int, int, int, int, int], ...
] = (
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
