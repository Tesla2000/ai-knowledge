from typing import Protocol

from dnd.character.stats import Stats


class SpellModifierContext(Protocol):
    @property
    def stats(self) -> Stats: ...

    @property
    def proficiency_bonus(self) -> int: ...
