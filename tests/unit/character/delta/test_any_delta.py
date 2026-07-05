from __future__ import annotations

import pytest

from dnd.character.delta.any_delta import _get_delta_type


@pytest.mark.unit
class TestGetDeltaType:
    def test_dict_with_delta_type_key(self) -> None:
        assert _get_delta_type({"delta_type": "SomeDelta"}) == "SomeDelta"

    def test_dict_without_delta_type_key_returns_none(self) -> None:
        assert _get_delta_type({"key": "value"}) is None

    def test_non_dict_non_delta_returns_none(self) -> None:
        assert _get_delta_type(42) is None

    def test_none_input_returns_none(self) -> None:
        assert _get_delta_type(None) is None
