import typing
from unittest.mock import MagicMock, patch

import pytest
from dnd.character.blueprint.building_blocks import LevelAssigner
from dnd.character.blueprint.building_blocks import SexAssigner
from dnd.character.blueprint.building_blocks.name_assigner import NameAssigner
from dnd.character.blueprint.building_blocks.age_assigner import AgeAssigner
from dnd.character.blueprint.simplified_blocks.simplified_blocks import (
    Classes,
    SimplifiedBlocks,
)
from dnd.character.checkpoint import IncrementChain, MemoryStorage
from dnd.choices.sex import Sex
from dnd.server.app import EXAMPLES, _get_union_schema, create_app
from frozendict import frozendict
from dnd.choices.class_creation.character_class import Class
from starlette.testclient import TestClient


@pytest.fixture
def storage():
    return MemoryStorage()


@pytest.fixture
def client(storage):
    return TestClient(create_app(storage))


@pytest.mark.unit
class TestServerApp:
    def test_root_redirects(self, client: TestClient) -> None:
        response = client.get("/", follow_redirects=False)
        assert response.status_code == 307
        assert response.headers["location"] == "/docs"

    def test_health_endpoint(self, client: TestClient) -> None:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

    def test_building_blocks_endpoint(self, client: TestClient) -> None:
        response = client.get("/building_blocks")
        assert response.status_code == 200
        data = response.json()
        assert "building_blocks" in data
        assert len(data["building_blocks"]) > 0

    def test_simplified_templates_endpoint(self, client: TestClient) -> None:
        response = client.get("/simplified_templates")
        assert response.status_code == 200
        data = response.json()
        assert "templates" in data
        assert len(data["templates"]) == 3

    def test_schema_endpoint(self, client: TestClient) -> None:
        response = client.get("/schema/simplified-blocks")
        assert response.status_code == 200
        data = response.json()
        assert "properties" in data
        assert "classes" in data["properties"]

    def test_create_character_simple(self, client: TestClient) -> None:
        response = client.post(
            "/create_character",
            json={
                "building_blocks": {
                    "classes": {"class_levels": {"Wizard": 1}},
                    "block_type": SimplifiedBlocks.__name__,
                },
                "increment_chain": {},
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["error"] is None

    def test_create_character_invalid_blocks(self, client: TestClient) -> None:
        response = client.post(
            "/create_character",
            json={
                "building_blocks": {"block_type": "NonExistentBlock"},
                "increment_chain": {},
            },
        )
        assert response.status_code == 422

    def test_create_character_incomplete_build(self, client: TestClient) -> None:
        block = SexAssigner(sex=Sex.MALE)
        response = client.post(
            "/create_character",
            json={
                "building_blocks": block.model_dump(mode="json"),
                "increment_chain": IncrementChain().model_dump(mode="json"),
            },
        )
        assert response.status_code == 422

    def test_create_character_stores_chain(
        self, client: TestClient, storage: MemoryStorage
    ) -> None:
        response = client.post(
            "/create_character",
            json={
                "building_blocks": {
                    "classes": {"class_levels": {"Wizard": 1}},
                    "block_type": SimplifiedBlocks.__name__,
                },
                "increment_chain": IncrementChain().model_dump(mode="json"),
            },
        )
        assert response.status_code == 200
        assert len(storage.list_chains()) > 0

    def test_format_simplified_with_defaults(self, client: TestClient) -> None:
        blocks = SimplifiedBlocks(
            classes=Classes(class_levels=frozendict({Class.WIZARD: 1}))
        )
        response = client.post(
            "/format_simplified?show_defaults=true",
            json=blocks.model_dump(exclude={"blocks"}, mode="json"),
        )
        assert response.status_code == 200

    def test_format_simplified_without_defaults(self, client: TestClient) -> None:
        blocks = SimplifiedBlocks(
            classes=Classes(class_levels=frozendict({Class.WIZARD: 1}))
        )
        response = client.post(
            "/format_simplified?show_defaults=false",
            json=blocks.model_dump(exclude={"blocks"}, mode="json"),
        )
        assert response.status_code == 200
        data = response.json()
        assert "block_type" in data

    def test_format_simplified_invalid(self, client: TestClient) -> None:
        response = client.post(
            "/format_simplified",
            json={"invalid": "data"},
        )
        assert response.status_code == 422


@pytest.mark.unit
class TestGetUnionSchema:
    def test_non_union_returns_none(self) -> None:
        result = _get_union_schema(int, "field")
        assert result is None

    def test_union_of_non_blocks_returns_none(self) -> None:
        annotation = typing.Union[int, str]
        result = _get_union_schema(annotation, "field")
        assert result is None

    def test_union_with_non_serializable_member_skips_it(self) -> None:
        annotation = typing.Union[int, SexAssigner]
        result = _get_union_schema(annotation, "field")
        assert result is not None
        assert isinstance(result["properties"], dict)
        assert isinstance(result["properties"]["block_type"], dict)
        assert (
            SexAssigner.get_block_type() in result["properties"]["block_type"]["enum"]
        )

    def test_cycle_detection_returns_none(self) -> None:
        annotation = typing.Union[SexAssigner, LevelAssigner]
        visited: set[object] = {annotation}
        result = _get_union_schema(annotation, "field", visited)
        assert result is None

    def test_nested_union_field_added_to_properties(self) -> None:
        inner_union = typing.Union[NameAssigner, AgeAssigner]
        mock_field = MagicMock()
        mock_field.annotation = inner_union
        extended_fields = {**SexAssigner.model_fields, "resolver": mock_field}

        annotation = typing.Union[SexAssigner, LevelAssigner]
        with patch.object(SexAssigner, "model_fields", extended_fields):
            result = _get_union_schema(annotation, "field")
        assert result is not None
        assert isinstance(result["properties"], dict)
        assert "resolver" in result["properties"]

    def test_duplicate_nested_field_not_overwritten(self) -> None:
        inner_union = typing.Union[NameAssigner, AgeAssigner]
        mock_field = MagicMock()
        mock_field.annotation = inner_union
        sex_fields = {**SexAssigner.model_fields, "resolver": mock_field}
        level_fields = {**LevelAssigner.model_fields, "resolver": mock_field}

        annotation = typing.Union[SexAssigner, LevelAssigner]
        with (
            patch.object(SexAssigner, "model_fields", sex_fields),
            patch.object(LevelAssigner, "model_fields", level_fields),
        ):
            result = _get_union_schema(annotation, "field")
        assert result is not None
        assert isinstance(result["properties"], dict)
        assert "resolver" in result["properties"]

    def test_examples_are_valid(self, client: TestClient) -> None:
        for example in EXAMPLES:
            response = client.post(
                "/create_character",
                json={
                    "building_blocks": example,
                    "increment_chain": IncrementChain().model_dump(mode="json"),
                },
            )
            assert response.status_code == 200

    def test_create_character_with_increment_chain(self, client: TestClient) -> None:
        first = client.post(
            "/create_character",
            json={
                "building_blocks": {
                    "classes": {"class_levels": {"Wizard": 1}},
                    "block_type": SimplifiedBlocks.__name__,
                },
                "increment_chain": IncrementChain().model_dump(mode="json"),
            },
        )
        assert first.status_code == 200
        chain = first.json()["increment_chain"]
        second = client.post(
            "/create_character",
            json={
                "building_blocks": {
                    "classes": {"class_levels": {"Wizard": 1}},
                    "block_type": SimplifiedBlocks.__name__,
                },
                "increment_chain": chain,
            },
        )
        assert second.status_code == 200

    def test_blocks_page_redirects(self, client: TestClient) -> None:
        response = client.get("/blocks", follow_redirects=False)
        assert response.status_code == 307

    def test_builder_page_redirects(self, client: TestClient) -> None:
        response = client.get("/builder", follow_redirects=False)
        assert response.status_code == 307

    def test_create_character_invalid_increment_chain(self, client: TestClient) -> None:
        response = client.post(
            "/create_character",
            json={
                "building_blocks": {
                    "classes": {"class_levels": {"Wizard": 1}},
                    "block_type": SimplifiedBlocks.__name__,
                },
                "increment_chain": {"increments": [{"delta_type": "NonExistentDelta"}]},
            },
        )
        assert response.status_code == 422
