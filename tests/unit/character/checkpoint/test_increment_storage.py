from __future__ import annotations

from pathlib import Path
from uuid import uuid4

import pytest

from dnd.character.checkpoint.increment_chain import IncrementChain
from dnd.character.checkpoint.increment_storage import (
    FileIncrementStorage,
    MemoryStorage,
)


@pytest.mark.unit
class TestFileIncrementStorage:
    def test_init_creates_directory(self, tmp_path: Path) -> None:
        storage_dir = tmp_path / "increments"
        assert not storage_dir.exists()
        FileIncrementStorage(storage_dir)
        assert storage_dir.exists()

    def test_save_and_load_roundtrip(self, tmp_path: Path) -> None:
        storage = FileIncrementStorage(tmp_path)
        chain_id = uuid4()
        chain = IncrementChain()
        storage.save_chain(chain_id, chain)
        loaded = storage.load_chain(chain_id)
        assert loaded.increments == chain.increments

    def test_load_missing_chain_raises(self, tmp_path: Path) -> None:
        storage = FileIncrementStorage(tmp_path)
        missing_id = uuid4()
        with pytest.raises(ValueError, match=str(missing_id)):
            storage.load_chain(missing_id)

    def test_delete_existing_chain_returns_true(self, tmp_path: Path) -> None:
        storage = FileIncrementStorage(tmp_path)
        chain_id = uuid4()
        storage.save_chain(chain_id, IncrementChain())
        assert storage.delete_chain(chain_id) is True

    def test_delete_missing_chain_returns_false(self, tmp_path: Path) -> None:
        storage = FileIncrementStorage(tmp_path)
        assert storage.delete_chain(uuid4()) is False

    def test_list_chains_empty(self, tmp_path: Path) -> None:
        storage = FileIncrementStorage(tmp_path)
        assert storage.list_chains() == []

    def test_list_chains_after_save(self, tmp_path: Path) -> None:
        storage = FileIncrementStorage(tmp_path)
        chain_id = uuid4()
        storage.save_chain(chain_id, IncrementChain())
        chains = storage.list_chains()
        assert chain_id in chains

    def test_chain_exists_true(self, tmp_path: Path) -> None:
        storage = FileIncrementStorage(tmp_path)
        chain_id = uuid4()
        storage.save_chain(chain_id, IncrementChain())
        assert storage.chain_exists(chain_id) is True

    def test_chain_exists_false(self, tmp_path: Path) -> None:
        storage = FileIncrementStorage(tmp_path)
        assert storage.chain_exists(uuid4()) is False

    def test_delete_removes_from_list(self, tmp_path: Path) -> None:
        storage = FileIncrementStorage(tmp_path)
        chain_id = uuid4()
        storage.save_chain(chain_id, IncrementChain())
        storage.delete_chain(chain_id)
        assert chain_id not in storage.list_chains()


@pytest.mark.unit
class TestMemoryStorageEdgeCases:
    def test_load_missing_chain_raises(self) -> None:
        storage = MemoryStorage()
        missing_id = uuid4()
        with pytest.raises(ValueError, match="chain_ids"):
            storage.load_chain(missing_id)

    def test_delete_existing_chain_returns_true(self) -> None:
        storage = MemoryStorage()
        chain_id = uuid4()
        storage.save_chain(chain_id, IncrementChain())
        assert storage.delete_chain(chain_id) is True

    def test_delete_missing_chain_returns_false(self) -> None:
        storage = MemoryStorage()
        assert storage.delete_chain(uuid4()) is False

    def test_chain_exists_true(self) -> None:
        storage = MemoryStorage()
        chain_id = uuid4()
        storage.save_chain(chain_id, IncrementChain())
        assert storage.chain_exists(chain_id) is True

    def test_chain_exists_false(self) -> None:
        storage = MemoryStorage()
        assert storage.chain_exists(uuid4()) is False
