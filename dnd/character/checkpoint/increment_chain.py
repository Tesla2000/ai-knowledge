from __future__ import annotations

from collections.abc import Iterator
from typing import Self

from dnd.character.delta import AnyDelta
from dnd.character.delta.delta import Delta
from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


class IncrementChain(BaseModel):
    """Ordered sequence of deltas representing a build process.

    Maintains a linear history of the character build, enabling
    restoration to any point and branching from increments.
    """

    model_config = ConfigDict(frozen=True)

    increments: tuple[AnyDelta, ...] = Field(
        default_factory=tuple,
        description="Ordered sequence of build deltas",
    )

    def get_increment(self, index: int) -> Delta | None:
        """Get increment at specific index."""
        if 0 <= index < len(self.increments):
            return self.increments[index]
        return None

    def get_latest(self) -> Delta | None:
        """Get the most recent increment."""
        if self.increments:
            return self.increments[-1]
        return None

    def add_increment(self, increment: Delta) -> Self:
        """Add a new delta to the chain (returns new instance)."""
        return self.model_copy(update={"increments": self.increments + (increment,)})

    def truncate_to(self, index: int) -> Self:
        """Create new chain containing only increments up to (and including) index."""
        if index < 0 or index > len(self.increments):
            raise IndexError(f"Increment index {index} out of range")
        return self.model_copy(update={"increments": self.increments[:index]})

    def length(self) -> int:
        """Return number of increments in chain."""
        return len(self.increments)

    def __len__(self) -> int:
        return self.length()

    def iter_deltas(self) -> Iterator[Delta]:
        """Iterate over deltas in order."""
        return iter(self.increments)
