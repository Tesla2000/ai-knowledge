from __future__ import annotations

from collections.abc import Iterator
from typing import Optional
from typing import Self

from dnd.character.blueprint.blueprint import Blueprint
from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


class IncrementChain(BaseModel):
    """Ordered sequence of increments representing a build process.

    Maintains a linear history of the character build, enabling
    restoration to any point and branching from increments.
    """

    model_config = ConfigDict(frozen=True)

    increments: tuple[Blueprint, ...] = Field(
        default_factory=tuple,
        description="Ordered sequence of build increments",
    )

    def get_increment(self, index: int) -> Optional[Blueprint]:
        """Get increment at specific index.

        Args:
            index: Increment index (0-based)

        Returns:
            Increment or None if index out of range
        """
        if 0 <= index < len(self.increments):
            return self.increments[index]
        return None

    def get_latest(self) -> Optional[Blueprint]:
        """Get the most recent increment."""
        if self.increments:
            return self.increments[-1]
        return None

    def add_increment(self, increment: Blueprint) -> Self:
        """Add a new increment to the chain (returns new instance).

        Args:
            increment: New increment to append

        Returns:
            New IncrementChain with increment added
        """
        return IncrementChain(increments=self.increments + (increment,))

    def truncate_to(self, index: int) -> Self:
        """Create new chain containing only increments up to (and including) index.

        Args:
            index: Last increment index to keep (inclusive)

        Returns:
            New IncrementChain with truncated history
        """
        if index < 0 or index > len(self.increments):
            raise IndexError(f"Increment index {index} out of range")
        return IncrementChain(increments=self.increments[:index])

    def length(self) -> int:
        """Return number of increments in chain."""
        return len(self.increments)

    def __len__(self) -> int:
        return self.length()

    def __iter__(self) -> Iterator[Blueprint]:
        """Iterate over increments in order."""
        return iter(self.increments)
