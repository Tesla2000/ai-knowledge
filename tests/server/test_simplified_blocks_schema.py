from dnd_character_creator.character.blueprint.building_blocks.building_block import (
    BLOCK_TYPE_FIELD_NAME,
)
from tests.server.test_client import TestClient


class TestSimplifiedBlocksSchema(TestClient):
    def test_schema_endpoint_returns_200(self, client):
        """Test that /schema/simplified-blocks endpoint is accessible."""
        response = client.get("/schema/simplified-blocks")
        assert response.status_code == 200

    def test_schema_structure(self, client):
        """Test that schema has correct JSON Schema structure."""
        response = client.get("/schema/simplified-blocks")
        schema = response.json()

        assert schema["$schema"] == "http://json-schema.org/draft-07/schema#"
        assert schema["title"] == "SimplifiedBlocks"
        assert schema["type"] == "object"
        assert "properties" in schema
        assert "required" in schema
        assert schema["additionalProperties"] is True

    def test_schema_includes_classes(self, client):
        """Test that schema includes classes field."""
        response = client.get("/schema/simplified-blocks")
        schema = response.json()

        assert "classes" in schema["properties"]
        assert "classes" in schema["required"]

        classes_prop = schema["properties"]["classes"]
        assert "class_levels" in classes_prop["properties"]

    def test_schema_includes_stats_priority(self, client):
        """Test that schema includes stats_priority field."""
        response = client.get("/schema/simplified-blocks")
        schema = response.json()

        assert "stats_priority" in schema["properties"]
        stats_priority_prop = schema["properties"]["stats_priority"]

        # Should be an array of 6 Statistic enums
        assert (
            stats_priority_prop["type"] == "array"
            or "prefixItems" in stats_priority_prop
        )

    def test_schema_includes_union_fields(self, client):
        """Test that schema includes Union type fields with block_type validation."""
        response = client.get("/schema/simplified-blocks")
        schema = response.json()

        # Check for common Union fields (only actual Union types)
        union_fields = [
            "language_choice_resolver",
            "skill_choice_resolver",
            "feat_choice_resolver",
            "race_assigner",
            "equipment_chooser",
        ]

        for field in union_fields:
            assert field in schema["properties"], f"Missing {field}"
            field_schema = schema["properties"][field]

            # Each Union field should be an object with block_type
            assert field_schema["type"] == "object"
            assert BLOCK_TYPE_FIELD_NAME in field_schema["properties"]

            # block_type should have enum of possible values
            block_type_schema = field_schema["properties"][
                BLOCK_TYPE_FIELD_NAME
            ]
            assert block_type_schema["type"] == "string"
            assert "enum" in block_type_schema
            assert len(block_type_schema["enum"]) > 0

    def test_block_type_enum_values(self, client):
        """Test that block_type enum contains expected values."""
        response = client.get("/schema/simplified-blocks")
        schema = response.json()

        # Check language_choice_resolver has expected block types
        lang_resolver = schema["properties"]["language_choice_resolver"]
        block_types = lang_resolver["properties"][BLOCK_TYPE_FIELD_NAME][
            "enum"
        ]

        assert {
            "RandomLanguageChoiceResolver",
            "AILanguageChoiceResolver",
        } == set(block_types)

        # Check skill_choice_resolver
        skill_resolver = schema["properties"]["skill_choice_resolver"]
        block_types = skill_resolver["properties"][BLOCK_TYPE_FIELD_NAME][
            "enum"
        ]

        assert set(block_types) == {
            "RandomSkillChoiceResolver",
            "AISkillChoiceResolver",
        }

    def test_nested_union_validation(self, client):
        """Test that nested Union fields are also validated recursively."""
        response = client.get("/schema/simplified-blocks")
        schema = response.json()

        # Check if any Union fields have nested Union fields
        # (This depends on the actual structure, but we can at least verify
        # the schema is properly structured for nested validation)
        for field_name, field_schema in schema["properties"].items():
            if (
                isinstance(field_schema, dict)
                and field_schema.get("type") == "object"
            ):
                # If it has block_type, it should allow additional properties
                if BLOCK_TYPE_FIELD_NAME in field_schema.get("properties", {}):
                    assert (
                        field_schema.get("additionalProperties") is True
                    ), f"{field_name} should allow additional properties"

    def test_schema_required_fields(self, client):
        """Test that only classes is required, other fields are optional."""
        response = client.get("/schema/simplified-blocks")
        schema = response.json()

        # Only classes should be required
        assert schema["required"] == ["classes"]

    def test_static_schema_matches_runtime_schema(self, client):
        """Verify pre-generated static schema matches runtime endpoint."""
        import json
        from pathlib import Path

        # Get runtime schema from endpoint
        runtime_response = client.get("/schema/simplified-blocks")
        runtime_schema = runtime_response.json()

        # Load static schema file
        static_dir = Path(__file__).parent.parent / "static"
        static_file = static_dir / "simplified-blocks-schema.json"

        if not static_file.exists():
            import pytest

            pytest.skip(
                "Static schema not generated yet (run scripts/generate_schema.py)"
            )

        with static_file.open() as f:
            static_schema = json.load(f)

        # Schemas should match exactly
        assert (
            static_schema == runtime_schema
        ), "Static and runtime schemas differ"
