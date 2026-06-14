from __future__ import annotations

from dnd.character.blueprint.simplified_blocks import (
    SimplifiedBlocks,
)
from dnd.character.blueprint.simplified_blocks.simplified_blocks import (
    Classes,
)
from dnd.character.checkpoint import IncrementChain
from dnd.choices.class_creation.character_class import Class
from tests.server.test_client import TestClient


class TestSimplifiedBuilder(TestClient):
    def test_simplified_block_success(self, client):
        response = client.post(
            "/create_character",
            json={
                "building_blocks": SimplifiedBlocks(
                    classes=Classes(class_levels={Class.WIZARD: 1})
                ).model_dump(exclude={"blocks"}),
                "increment_chain": IncrementChain().model_dump(mode="json"),
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert "increment_chain" in data
        assert "error" in data
        assert data["error"] is None
