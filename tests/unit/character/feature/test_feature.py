from __future__ import annotations

import types
import pytest
from pydantic import TypeAdapter

from dnd.character.feature.feature import Feature
from dnd.other_profficiencies import ToolProficiency


@pytest.mark.unit
class TestFeatureNormalize:
    def test_non_dict_input_passes_through(self) -> None:
        original = Feature()
        result = Feature.model_validate(original)
        assert isinstance(result, Feature)

    def test_tool_proficiency_in_skill_field_moves_to_tool(self) -> None:
        data = {"skill_proficiency_gain": ToolProficiency.HERBALISM_KIT}
        f = Feature.model_validate(data)
        assert f.tool_proficiency_gain == ToolProficiency.HERBALISM_KIT
        assert f.skill_proficiency_gain is None

    def test_non_dict_input_returns_early(self) -> None:
        ta = TypeAdapter(Feature)
        ns = types.SimpleNamespace()
        result = ta.validate_python(ns, from_attributes=True)
        assert isinstance(result, Feature)
