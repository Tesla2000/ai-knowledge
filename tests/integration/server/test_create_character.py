from __future__ import annotations

from unittest.mock import patch

import pytest
from dnd.character.blueprint.building_blocks import (
    LevelAssigner,
)
from dnd.character.blueprint.building_blocks import (
    SexAssigner,
)
from dnd.character.checkpoint import IncrementChain
from dnd.choices.sex import Sex
from dnd.server.app import EXAMPLES
from dnd.server.app import _building_blocks_creator
from tests.integration.server.test_client import TestClient


def _dump(blocks: tuple) -> list:
    return _building_blocks_creator.dump_python(blocks, mode="json")


class TestCreateCharacter(TestClient):
    def test_create_character_success(self, client, storage, building_blocks):
        """Test successful character creation."""

        response = client.post(
            "/create_character",
            json={
                "building_blocks": _dump(building_blocks),
                "increment_chain": IncrementChain().model_dump(mode="json"),
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert "increment_chain" in data
        assert "error" in data
        assert data["error"] is None

    def test_create_character_with_existing_increment_chain(
        self, client, storage, building_blocks
    ):
        """Test character creation resuming from existing increment chain."""

        first_response = client.post(
            "/create_character",
            json={
                "building_blocks": _dump(building_blocks),
                "increment_chain": IncrementChain().model_dump(mode="json"),
            },
        )

        assert first_response.status_code == 200
        first_data = first_response.json()
        first_chain = first_data["increment_chain"]

        extended_blocks = building_blocks + (SexAssigner(sex=Sex.MALE),)

        second_response = client.post(
            "/create_character",
            json={
                "building_blocks": _dump(extended_blocks),
                "increment_chain": first_chain,
            },
        )

        assert second_response.status_code == 200
        second_data = second_response.json()
        assert len(second_data["increment_chain"]["increments"]) > len(
            first_chain["increments"]
        )

    def test_create_character_error_handling(self, client, building_blocks):
        """Test that errors during character building are handled properly."""
        with patch.object(
            LevelAssigner,
            LevelAssigner.get_change.__name__,
            side_effect=ValueError("Test error"),
        ) as mock_level_assigner:
            response = client.post(
                "/create_character",
                json={
                    "building_blocks": _dump(building_blocks),
                    "increment_chain": IncrementChain().model_dump(mode="json"),
                },
            )
            mock_level_assigner.assert_called_once()
            assert response.status_code == 422

    def test_create_character_empty_building_blocks(self, client):
        """Test character creation with empty building blocks."""
        response = client.post(
            "/create_character",
            json={
                "building_blocks": _dump(()),
                "increment_chain": IncrementChain().model_dump(mode="json"),
            },
        )

        assert response.status_code == 422

    def test_increment_chain_stored_in_storage(self, client, storage, building_blocks):
        """Test that increment chains are properly stored."""

        response = client.post(
            "/create_character",
            json={
                "building_blocks": _dump(building_blocks),
                "increment_chain": IncrementChain().model_dump(mode="json"),
            },
        )

        assert response.status_code == 200
        chains = storage.list_chains()
        assert len(chains) > 0

    def test_multiple_character_creations(self, client, storage):
        """Test creating multiple characters."""
        for i in range(3):
            blocks = (
                SexAssigner(sex=Sex.MALE if i % 2 == 0 else Sex.FEMALE),
                LevelAssigner(level=i + 1),
            )

            response = client.post(
                "/create_character",
                json={
                    "building_blocks": _dump(blocks),
                    "increment_chain": IncrementChain().model_dump(mode="json"),
                },
            )

            assert response.status_code == 422

        chains = storage.list_chains()
        assert len(chains) == 3

    def test_response_model_structure(self, client):
        """Test that response follows expected model structure."""
        blocks = (
            SexAssigner(sex=Sex.MALE),
            LevelAssigner(level=1),
        )

        response = client.post(
            "/create_character",
            json={
                "building_blocks": _dump(blocks),
                "increment_chain": IncrementChain().model_dump(mode="json"),
            },
        )

        data = response.json()
        assert "character" in data
        assert "increment_chain" in data
        assert "error" in data
        assert isinstance(data["increment_chain"], dict)
        assert "increments" in data["increment_chain"]

    def test_create_character(self, client):
        response = client.post(
            "/create_character",
            json={
                "building_blocks": EXAMPLES[0],
                "increment_chain": {},
            },
        )
        assert response.status_code == 200

    def test_invalid_building_blocks_returns_422(self, client):
        response = client.post(
            "/create_character",
            json={
                "building_blocks": [{"type": "invalid_block_type"}],
                "increment_chain": {},
            },
        )
        assert response.status_code == 422

    @pytest.mark.parametrize("example", EXAMPLES)
    def test_create_character_examples(self, example, client):
        response = client.post(
            "/create_character",
            json={
                "building_blocks": example,
                "increment_chain": IncrementChain().model_dump(mode="json"),
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "character" in data
        assert "increment_chain" in data
        assert "error" in data
        assert data["error"] is None
        assert isinstance(data["increment_chain"], dict)
        assert "increments" in data["increment_chain"]
