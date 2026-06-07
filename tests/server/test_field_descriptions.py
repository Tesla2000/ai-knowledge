"""Test that Field descriptions are properly set and displayed via the API."""

<<<<<<<< HEAD:tests/server/test_field_descriptions.py
from tests.server.test_client import TestClient
========
from dnd.server.tests.test_client import TestClient
>>>>>>>> 34edfe5 (Rename to dnd):dnd/server/tests/test_field_descriptions.py


class TestFieldDescriptions(TestClient):
    """Test suite for validating Field descriptions in building blocks."""

    def test_building_blocks_endpoint_returns_field_descriptions(self, client):
        """Test that the /building_blocks endpoint returns field descriptions."""
        response = client.get("/building_blocks")
        assert response.status_code == 200

        data = response.json()
        assert "building_blocks" in data
        building_blocks = data["building_blocks"]

        # Verify we have building blocks
        assert len(building_blocks) > 0

        # Find blocks and verify their field descriptions
        blocks_by_name = {block["name"]: block for block in building_blocks}

        # Test 1: AIAllChoicesResolver.blocks
        if "AIAllChoicesResolver" in blocks_by_name:
            ai_all_choices = blocks_by_name["AIAllChoicesResolver"]
            assert "blocks" in ai_all_choices["fields"]
            assert ai_all_choices["fields"]["blocks"]["description"] == (
                "Ordered building blocks: stat resolver, equipment chooser, "
                "optional feat resolver, and non-stat choices resolver"
            )

        # Test 2: AISubclassAssigner.llm
        if "AISubclassAssigner" in blocks_by_name:
            ai_subclass = blocks_by_name["AISubclassAssigner"]
            assert "llm" in ai_subclass["fields"]
            assert ai_subclass["fields"]["llm"]["description"] == (
                "Language model for making AI-powered decisions"
            )

        # Test 3: AIMagicalItemChooser.llm
        if "AIMagicalItemChooser" in blocks_by_name:
            ai_magical = blocks_by_name["AIMagicalItemChooser"]
            assert "llm" in ai_magical["fields"]
            assert ai_magical["fields"]["llm"]["description"] == (
                "Language model for making AI-powered decisions"
            )

        # Test 4-6: LLMSpellAssigner fields
        if "LLMSpellAssigner" in blocks_by_name:
            llm_spell = blocks_by_name["LLMSpellAssigner"]
            assert "class_" in llm_spell["fields"]
            assert llm_spell["fields"]["class_"]["description"] == (
                "Character class for spell assignment"
            )
            assert "llm" in llm_spell["fields"]
            assert llm_spell["fields"]["llm"]["description"] == (
                "Language model for making AI-powered decisions"
            )
            assert "character_description" in llm_spell["fields"]
            assert llm_spell["fields"]["character_description"][
                "description"
            ] == ("Additional character context for AI spell selection")

        # Test 7: RandomInitialDataFiller.seed
        if "RandomInitialDataFiller" in blocks_by_name:
            random_filler = blocks_by_name["RandomInitialDataFiller"]
            assert "seed" in random_filler["fields"]
            assert random_filler["fields"]["seed"]["description"] == (
                "Optional seed for reproducible random selection"
            )

        # Test 8-9: AIBaseBuilderAssigner and AIPartialBuilderAssigner.llm
        # These inherit from AIBuilderBase which has the llm field
        for block_name in [
            "AIBaseBuilderAssigner",
            "AIPartialBuilderAssigner",
        ]:
            if block_name in blocks_by_name:
                block = blocks_by_name[block_name]
                assert "llm" in block["fields"]
                assert block["fields"]["llm"]["description"] == (
                    "Language model for making AI-powered decisions"
                )

        # Test 10-11: RaceAssigner.race and subrace
        if "RaceAssigner" in blocks_by_name:
            race_assigner = blocks_by_name["RaceAssigner"]
            assert "race" in race_assigner["fields"]
            assert race_assigner["fields"]["race"]["description"] == (
                "Character's race selection"
            )
            assert "subrace" in race_assigner["fields"]
            assert race_assigner["fields"]["subrace"]["description"] == (
                "Character's subrace selection"
            )

        # Test 12: AIToolProficiencyChoiceResolver.llm
        if "AIToolProficiencyChoiceResolver" in blocks_by_name:
            ai_tool = blocks_by_name["AIToolProficiencyChoiceResolver"]
            assert "llm" in ai_tool["fields"]
            assert ai_tool["fields"]["llm"]["description"] == (
                "Language model for making AI-powered decisions"
            )

        # Test 13: AISkillChoiceResolver.llm
        if "AISkillChoiceResolver" in blocks_by_name:
            ai_skill = blocks_by_name["AISkillChoiceResolver"]
            assert "llm" in ai_skill["fields"]
            assert ai_skill["fields"]["llm"]["description"] == (
                "Language model for making AI-powered decisions"
            )

        # Test 14: AILanguageChoiceResolver.llm
        if "AILanguageChoiceResolver" in blocks_by_name:
            ai_language = blocks_by_name["AILanguageChoiceResolver"]
            assert "llm" in ai_language["fields"]
            assert ai_language["fields"]["llm"]["description"] == (
                "Language model for making AI-powered decisions"
            )

        # Test 15: AIStatChoiceResolver.llm
        if "AIStatChoiceResolver" in blocks_by_name:
            ai_stat = blocks_by_name["AIStatChoiceResolver"]
            assert "llm" in ai_stat["fields"]
            assert ai_stat["fields"]["llm"]["description"] == (
                "Language model for making AI-powered decisions"
            )

        # Test 16: AIFeatChoiceResolver.llm
        if "AIFeatChoiceResolver" in blocks_by_name:
            ai_feat = blocks_by_name["AIFeatChoiceResolver"]
            assert "llm" in ai_feat["fields"]
            assert ai_feat["fields"]["llm"]["description"] == (
                "Language model for making AI-powered decisions"
            )

        # Test 17: AIEquipmentChooser.llm
        if "AIEquipmentChooser" in blocks_by_name:
            ai_equipment = blocks_by_name["AIEquipmentChooser"]
            assert "llm" in ai_equipment["fields"]
            assert ai_equipment["fields"]["llm"]["description"] == (
                "Language model for making AI-powered decisions"
            )

    def test_all_llm_fields_have_same_description(self, client):
        """Test that all llm fields across building blocks have consistent descriptions."""
        response = client.get("/building_blocks")
        assert response.status_code == 200

        data = response.json()
        building_blocks = data["building_blocks"]

        # Collect all llm field descriptions
        llm_descriptions = []
        for block in building_blocks:
            if "llm" in block["fields"]:
                llm_descriptions.append(
                    (block["name"], block["fields"]["llm"]["description"])
                )

        # Verify they all have the same description
        expected_description = "Language model for making AI-powered decisions"
        for block_name, description in llm_descriptions:
            assert (
                description == expected_description
            ), f"Block {block_name} has incorrect llm description: {description}"

    def test_no_empty_field_descriptions(self, client):
        """Test that important fields have non-empty descriptions."""
        response = client.get("/building_blocks")
        assert response.status_code == 200

        data = response.json()
        building_blocks = data["building_blocks"]

        # List of critical fields that should have descriptions
        critical_fields = {
            "llm",
            "seed",
            "race",
            "subrace",
            "class_",
            "character_description",
            "blocks",
        }

        for block in building_blocks:
            block_name = block["name"]
            for field_name, field_info in block["fields"].items():
                if field_name in critical_fields:
                    assert field_info["description"], (
                        f"Field '{field_name}' in block '{block_name}' "
                        f"has an empty description"
                    )
