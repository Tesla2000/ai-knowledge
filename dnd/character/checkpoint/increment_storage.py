from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from pathlib import Path
from uuid import UUID

from dnd.character.checkpoint.increment_chain import (
    IncrementChain,
)


class IncrementStorage(ABC):
    """Abstract interface for increment storage backends.

    Implementations can store build increments in files, databases, or other systems.
    """

    @abstractmethod
    def load_chain(self, chain_id: UUID) -> IncrementChain:
        """Load an increment chain by ID.

        Args:
            chain_id: Unique identifier for the chain

        Raises:
            ValueError: If not found

        Returns:
            IncrementChain
        """

    @abstractmethod
    def delete_chain(self, chain_id: UUID) -> bool:
        """Delete an increment chain by ID.

        Args:
            chain_id: Unique identifier for the chain

        Returns:
            True if deleted, False if not found
        """

    @abstractmethod
    def list_chains(self) -> list[UUID]:
        """List all available increment chain IDs.

        Returns:
            List of chain IDs
        """

    @abstractmethod
    def chain_exists(self, chain_id: UUID) -> bool:
        """Check if an increment chain exists.

        Args:
            chain_id: Unique identifier for the chain

        Returns:
            True if exists, False otherwise
        """


class FileIncrementStorage(IncrementStorage):
    """File-based increment storage implementation.

    Stores increment chains as JSON files in a specified directory.
    """

    def __init__(self, base_path: Path = Path(".build_increments")):
        """Initialize file storage.

        Args:
            base_path: Base directory for storing increment files
        """
        self._base_path = base_path
        self._base_path.mkdir(parents=True, exist_ok=True)

    def _get_file_path(self, chain_id: UUID) -> Path:
        """Get file path for a chain ID."""
        return self._base_path / f"{chain_id}.json"

    def save_chain(self, chain_id: UUID, chain: IncrementChain) -> None:
        """Save an increment chain to a JSON file."""
        file_path = self._get_file_path(chain_id)
        file_path.write_text(chain.model_dump_json())

    def load_chain(self, chain_id: UUID) -> IncrementChain:
        """Load an increment chain from a JSON file."""
        file_path = self._get_file_path(chain_id)
        if not file_path.exists():
            raise ValueError(
                f"File path corresponding to {chain_id=} not found"
            )
        return IncrementChain.model_validate_json(file_path.read_bytes())

    def delete_chain(self, chain_id: UUID) -> bool:
        """Delete an increment chain file."""
        file_path = self._get_file_path(chain_id)
        if file_path.exists():
            file_path.unlink()
            return True
        return False

    def list_chains(self) -> list[UUID]:
        """List all increment chain IDs in the directory."""
        return [
            UUID(p.stem) for p in self._base_path.glob("*.json") if p.is_file()
        ]

    def chain_exists(self, chain_id: UUID) -> bool:
        """Check if an increment chain file exists."""
        return self._get_file_path(chain_id).exists()


class MemoryStorage(IncrementStorage):
    """In-memory increment storage for testing and temporary use."""

    def __init__(self):
        """Initialize in-memory storage."""
        self._chains: dict[UUID, IncrementChain] = {}

    def save_chain(self, chain_id: UUID, chain: IncrementChain) -> None:
        """Save an increment chain to memory."""
        self._chains[chain_id] = chain

    def load_chain(self, chain_id: UUID) -> IncrementChain:
        """Load an increment chain from memory."""
        if chain_id not in self._chains:
            chain_ids = tuple(self._chains)
            raise ValueError(f"Chain id not in {chain_ids=}")
        return self._chains[chain_id]

    def delete_chain(self, chain_id: UUID) -> bool:
        """Delete an increment chain from memory."""
        if chain_id in self._chains:
            del self._chains[chain_id]
            return True
        return False

    def list_chains(self) -> list[UUID]:
        """List all increment chain IDs in memory."""
        return list(self._chains.keys())

    def chain_exists(self, chain_id: UUID) -> bool:
        """Check if an increment chain exists in memory."""
        return chain_id in self._chains
