from unittest.mock import patch

import pytest
from dnd.character.blueprint.building_blocks import (
    LevelAssigner,
)

from dnd.server.app import EXAMPLES
from dnd.server.app import _building_blocks_creator
from tests.integration.server.test_client import TestClient


def _dump(blocks: tuple) -> list:
    return _building_blocks_creator.dump_python(blocks, mode="json")


class TestCreateCharacter(TestClient):
    def test_create_character_success(self, client, building_blocks):
        response = client.post(
            "/create_character",
            json={"building_blocks": _dump(building_blocks)},
        )
        assert response.status_code == 200
        data = response.json()
        assert "error" in data
        assert data["error"] is None

    def test_create_character_error_handling(self, client, building_blocks):
        with patch.object(
            LevelAssigner,
            "apply",
            side_effect=ValueError("Test error"),
        ) as mock_apply:
            response = client.post(
                "/create_character",
                json={"building_blocks": _dump(building_blocks)},
            )
            mock_apply.assert_called_once()
            assert response.status_code == 422

    def test_create_character_empty_building_blocks(self, client):
        response = client.post(
            "/create_character",
            json={"building_blocks": _dump(())},
        )
        assert response.status_code == 422

    def test_create_character(self, client):
        response = client.post(
            "/create_character",
            json={"building_blocks": EXAMPLES[0]},
        )
        assert response.status_code == 200

    def test_invalid_building_blocks_returns_422(self, client):
        response = client.post(
            "/create_character",
            json={"building_blocks": [{"type": "invalid_block_type"}]},
        )
        assert response.status_code == 422

    @pytest.mark.parametrize("example", EXAMPLES)
    def test_create_character_examples(self, example, client):
        response = client.post(
            "/create_character",
            json={"building_blocks": example},
        )
        assert response.status_code == 200
        data = response.json()
        assert "character" in data
        assert "error" in data
        assert data["error"] is None
