import pytest
import dnd.server.app as _app_module
from unittest.mock import MagicMock
from dnd.character.blueprint.building_blocks.null_block import NullBlock
from dnd.server.app import create_app
from dnd.server.example_generators.example_building_blocks import (
    example_building_blocks,
)
from starlette.testclient import TestClient


@pytest.fixture
def client():
    return TestClient(create_app())


@pytest.mark.unit
class TestServerApp:
    def test_create_character_simple(
        self, client: TestClient, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        blocks = example_building_blocks()
        monkeypatch.setattr(
            _app_module,
            "_building_blocks_creator",
            MagicMock(validate_python=MagicMock(return_value=blocks)),
        )
        response = client.post("/create_character", json={"building_blocks": []})
        assert response.status_code == 200
        data = response.json()
        assert data["error"] is None

    def test_create_character_invalid_blocks(self, client: TestClient) -> None:
        response = client.post(
            "/create_character",
            json={"building_blocks": {"block_type": "NonExistentBlock"}},
        )
        assert response.status_code == 422

    def test_create_character_invalid_block_type(self, client: TestClient) -> None:
        response = client.post(
            "/create_character",
            json={"building_blocks": [{"type": "NonExistentBlock"}]},
        )
        assert response.status_code == 422

    def test_create_character_incomplete_build(self, client: TestClient) -> None:
        block = NullBlock()
        response = client.post(
            "/create_character",
            json={"building_blocks": block.model_dump(mode="json")},
        )
        assert response.status_code == 422

    def test_create_character_build_failure_returns_error(
        self, client: TestClient
    ) -> None:
        block = NullBlock()
        response = client.post(
            "/create_character",
            json={"building_blocks": [block.model_dump(mode="json")]},
        )
        assert response.status_code == 422
        data = response.json()
        assert data["error"] is not None

    def test_root_redirects_to_docs(self, client: TestClient) -> None:
        response = client.get("/", follow_redirects=False)
        assert response.status_code == 307
        assert response.headers["location"] == "/docs"
