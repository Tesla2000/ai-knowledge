from __future__ import annotations

from unittest.mock import patch

import pytest
from dnd_character_creator.character.blueprint.building_blocks import (
    CombinedBlock,
)
from dnd_character_creator.character.blueprint.building_blocks import (
    LevelAssigner,
)
from dnd_character_creator.character.blueprint.building_blocks import (
    SexAssigner,
)
from dnd_character_creator.character.blueprint.simplified_blocks import (
    SimplifiedBlocks,
)
from dnd_character_creator.character.checkpoint import IncrementChain
from dnd_character_creator.choices.sex import Sex
from dnd_character_creator.server.app import EXAMPLES
from dnd_character_creator.server.tests.test_client import TestClient


class TestCreateCharacter(TestClient):
    def test_root_redirects_to_docs(self, client):
        """Test that root path redirects to API documentation."""
        response = client.get("/", follow_redirects=False)
        assert response.status_code == 307
        assert response.headers["location"] == "/docs"

    def test_create_character_success(self, client, storage, building_blocks):
        """Test successful character creation."""

        response = client.post(
            "/create_character",
            json={
                "building_blocks": building_blocks.model_dump(mode="json"),
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
                "building_blocks": building_blocks.model_dump(mode="json"),
                "increment_chain": IncrementChain().model_dump(mode="json"),
            },
        )

        assert first_response.status_code == 200
        first_data = first_response.json()
        first_chain = first_data["increment_chain"]

        additional_blocks = CombinedBlock(
            blocks=(
                SexAssigner(
                    sex=Sex.MALE,
                ),
            )
        )

        second_response = client.post(
            "/create_character",
            json={
                "building_blocks": (
                    building_blocks + additional_blocks
                ).model_dump(mode="json"),
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
                    "building_blocks": building_blocks.model_dump(mode="json"),
                    "increment_chain": IncrementChain().model_dump(
                        mode="json"
                    ),
                },
            )
            mock_level_assigner.assert_called_once()
            assert response.status_code == 422

    def test_create_character_empty_building_blocks(self, client):
        """Test character creation with empty building blocks."""
        response = client.post(
            "/create_character",
            json={
                "building_blocks": CombinedBlock(blocks=()).model_dump(
                    mode="json"
                ),
                "increment_chain": IncrementChain().model_dump(mode="json"),
            },
        )

        assert response.status_code == 422

    def test_increment_chain_stored_in_storage(
        self, client, storage, building_blocks
    ):
        """Test that increment chains are properly stored."""

        response = client.post(
            "/create_character",
            json={
                "building_blocks": building_blocks.model_dump(mode="json"),
                "increment_chain": IncrementChain().model_dump(mode="json"),
            },
        )

        assert response.status_code == 200
        chains = storage.list_chains()
        assert len(chains) > 0

    def test_multiple_character_creations(self, client, storage):
        """Test creating multiple characters."""
        for i in range(3):
            building_blocks = CombinedBlock(
                blocks=(
                    SexAssigner(sex=Sex.MALE if i % 2 == 0 else Sex.FEMALE),
                    LevelAssigner(level=i + 1),
                )
            )

            response = client.post(
                "/create_character",
                json={
                    "building_blocks": building_blocks.model_dump(mode="json"),
                    "increment_chain": IncrementChain().model_dump(
                        mode="json"
                    ),
                },
            )

            assert response.status_code == 422

        chains = storage.list_chains()
        assert len(chains) == 3

    def test_response_model_structure(self, client):
        """Test that response follows expected model structure."""
        building_blocks = CombinedBlock(
            blocks=(
                SexAssigner(sex=Sex.MALE),
                LevelAssigner(level=1),
            )
        )

        response = client.post(
            "/create_character",
            json={
                "building_blocks": building_blocks.model_dump(mode="json"),
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
                "building_blocks": {
                    "classes": {"class_levels": {"Wizard": 13}},
                    "block_type": SimplifiedBlocks.get_block_type(),
                },
                "increment_chain": {},
            },
        )
        assert response.status_code == 200

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
