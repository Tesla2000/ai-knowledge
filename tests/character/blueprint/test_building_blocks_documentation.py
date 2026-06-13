"""Tests for building blocks documentation and API endpoint."""

import unittest

from dnd_character_creator.character.blueprint.building_blocks.building_block import (
    SerializableBlock,
)
from dnd_character_creator.server.app import app
from fastapi.testclient import TestClient
from subclass_getter import get_unique_subclasses


class TestBuildingBlocksDocumentation(unittest.TestCase):
    """Test that all building blocks have proper documentation."""

    def test_all_building_blocks_have_docstrings(self):
        """Ensure every building block has a docstring."""
        missing_docstrings = []

        for block_class in get_unique_subclasses(SerializableBlock):
            if not block_class.__doc__:
                missing_docstrings.append(block_class.__name__)

        self.assertEqual(
            [],
            missing_docstrings,
            f"The following building blocks are missing docstrings: {missing_docstrings}",
        )

    def test_all_building_blocks_have_field_descriptions(self):
        """Ensure all fields in building blocks have descriptions."""
        from dnd_character_creator.character.blueprint.building_blocks.building_block import (
            BLOCK_TYPE_FIELD_NAME,
        )

        missing_descriptions = []

        for block_class in get_unique_subclasses(SerializableBlock):
            for field_name, field_info in block_class.model_fields.items():
                if field_name == BLOCK_TYPE_FIELD_NAME:
                    continue  # Skip discriminator field

                if not field_info.description:
                    missing_descriptions.append(
                        f"{block_class.__name__}.{field_name}"
                    )

        self.assertEqual(
            [],
            missing_descriptions,
            f"The following fields are missing descriptions: {missing_descriptions}",
        )


class TestBuildingBlocksAPI(unittest.TestCase):
    """Test the /building_blocks API endpoint."""

    @classmethod
    def setUpClass(cls):
        """Set up test client."""
        cls.client = TestClient(app)

    def test_building_blocks_endpoint_returns_200(self):
        """Test that /building_blocks endpoint returns 200 OK."""
        response = self.client.get("/building_blocks")
        self.assertEqual(200, response.status_code)

    def test_building_blocks_endpoint_returns_json(self):
        """Test that /building_blocks endpoint returns JSON."""
        response = self.client.get("/building_blocks")
        self.assertEqual("application/json", response.headers["content-type"])

    def test_building_blocks_endpoint_returns_valid_structure(self):
        """Test that /building_blocks endpoint returns the expected structure."""
        response = self.client.get("/building_blocks")
        data = response.json()

        # Check top-level structure
        self.assertIn("building_blocks", data)
        self.assertIsInstance(data["building_blocks"], list)
        self.assertGreater(len(data["building_blocks"]), 0)

        # Check first block structure
        block = data["building_blocks"][0]
        self.assertIn("block_type", block)
        self.assertIn("name", block)
        self.assertIn("description", block)
        self.assertIn("fields", block)

        # Check that description is not empty
        self.assertTrue(block["description"])

        # Check fields structure
        self.assertIsInstance(block["fields"], dict)
        if len(block["fields"]) > 0:
            field_name = list(block["fields"].keys())[0]
            field = block["fields"][field_name]
            self.assertIn("type", field)
            self.assertIn("description", field)

    def test_building_blocks_are_sorted_alphabetically(self):
        """Test that building blocks are sorted alphabetically by name."""
        response = self.client.get("/building_blocks")
        data = response.json()

        names = [block["name"] for block in data["building_blocks"]]
        sorted_names = sorted(names)

        self.assertEqual(sorted_names, names)

    def test_static_html_page_exists(self):
        """Test that the static HTML page is accessible."""
        response = self.client.get("/static/building_blocks.html")
        self.assertEqual(200, response.status_code)
        self.assertIn("text/html", response.headers["content-type"])

    def test_blocks_redirect_works(self):
        """Test that /blocks redirects to the HTML page."""
        response = self.client.get("/blocks", follow_redirects=False)
        self.assertEqual(307, response.status_code)
        self.assertEqual(
            "/static/building_blocks.html", response.headers["location"]
        )

    def test_multiline_docstrings_preserved(self):
        """Test that multi-line docstrings preserve newlines."""
        response = self.client.get("/building_blocks")
        self.assertEqual(200, response.status_code)

        data = response.json()
        building_blocks = data["building_blocks"]

        # Find a block with a multi-line docstring (AIAllChoicesResolver has one)
        block = next(
            (
                b
                for b in building_blocks
                if b["name"] == "AIAllChoicesResolver"
            ),
            None,
        )
        self.assertIsNotNone(block, "AIAllChoicesResolver block not found")

        # Check that the description contains newlines
        description = block["description"]
        self.assertIn(
            "\n", description, "Multi-line docstring should preserve newlines"
        )

        # Check that it has multiple lines
        lines = description.split("\n")
        self.assertGreater(
            len(lines), 1, "Multi-line docstring should have multiple lines"
        )


if __name__ == "__main__":
    unittest.main()
